"""Germline and somatic calling with Strelka2: https://github.com/illumina/strelka
"""
import os
import sys

from bcbio import utils
from bcbio.distributed.transaction import file_transaction
from bcbio.pipeline import shared
from bcbio.pipeline import datadict as dd
from bcbio.provenance import do
from bcbio.variation import bedutils, joint, ploidy, vcfutils

def run(align_bams, items, ref_file, assoc_files, region, out_file):
    """Run strelka2 variant calling, either paired tumor/normal or germline calling.

    region can be a single region or list of multiple regions for multicore calling.
    """
    if vcfutils.is_paired_analysis(align_bams, items):
        paired = vcfutils.get_paired_bams(align_bams, items)
        assert paired.normal_bam, "Strelka2 requires a normal sample"
        call_file = _run_somatic(paired, ref_file, assoc_files, region, out_file)
    else:
        call_file = _run_germline(align_bams, items, ref_file,
                                  assoc_files, region, out_file)
    return call_file

def get_region_bed(region, items, out_file, want_gzip=True):
    """Retrieve BED file of regions to analyze, either single or multi-region.
    """
    variant_regions = bedutils.merge_overlaps(bedutils.population_variant_regions(items), items[0])
    target = shared.subset_variant_regions(variant_regions, region, out_file, items)
    if not target:
        raise ValueError("Need BED input for strelka2 regions: %s %s" % (region, target))
    if not isinstance(target, basestring) or not os.path.isfile(target):
        chrom, start, end = target
        target = "%s-regions.bed" % utils.splitext_plus(out_file)[0]
        with file_transaction(items[0], target) as tx_out_file:
            with open(tx_out_file, "w") as out_handle:
                out_handle.write("%s\t%s\t%s\n" % (chrom, start, end))
    out_file = bedutils.merge_overlaps(target, items[0], out_dir=os.path.dirname(out_file))
    if want_gzip:
        out_file += ".gz"
    return out_file

def _get_ploidy(regions, items, base_file):
    samples = [dd.get_sample_name(d) for d in items]
    out_file = "%s-ploidy.vcf" % utils.splitext_plus(base_file)[0]
    if not utils.file_exists(out_file) and not utils.file_exists(out_file + ".gz"):
        with file_transaction(items[0], out_file) as tx_outfile:
            with open(tx_outfile, "w") as h:
                h.write("##fileformat=VCFv4.1\n")
                h.write('##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">\n')
                h.write('##FORMAT=<ID=CN,Number=1,Type=Integer,Description="Copy number genotype for imprecise events">\n')
                h.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + "\t".join(samples) + "\n")
                for region in regions:
                    ploidies = [ploidy.get_ploidy([d], region) for d in items]
                    h.write("\t".join([region[0], str(region[1]), ".", "N", "<CNV>", ".", ".",
                                       "END=%s" % region[2], "CN"] + [str(x) for x in ploidies]) + "\n")
    return vcfutils.bgzip_and_index(out_file, items[0]["config"])

def _configure_germline(align_bams, items, ref_file, region, out_file, tx_work_dir):
    utils.safe_makedir(tx_work_dir)
    cmd = [sys.executable, os.path.realpath(utils.which("configureStrelkaGermlineWorkflow.py"))]
    cmd += ["--referenceFasta=%s" % ref_file,
            "--callRegions=%s" % get_region_bed(region, items, out_file),
            "--ploidy=%s" % _get_ploidy(shared.to_multiregion(region), items, out_file),
            "--runDir=%s" % tx_work_dir]
    cmd += ["--bam=%s" % b for b in align_bams]
    if any(dd.get_coverage_interval(d) not in ["genome"] for d in items):
        cmd += ["--targeted"]
    do.run(cmd, "Configure Strelka2 germline calling: %s" % (", ".join([dd.get_sample_name(d) for d in items])))
    return os.path.join(tx_work_dir, "runWorkflow.py")

def _run_germline(align_bams, items, ref_file, assoc_files, region, out_file):
    if not utils.file_exists(out_file):
        work_dir = "%s-work" % utils.splitext_plus(out_file)[0]
        with file_transaction(items[0], work_dir) as tx_work_dir:
            workflow_file = _configure_germline(align_bams, items, ref_file, region, out_file, tx_work_dir)
            _run_workflow(items[0], workflow_file, tx_work_dir)
        raw_file = os.path.join(work_dir, "results", "variants",
                                "genome.vcf.gz" if joint.want_gvcf(items) else "variants.vcf.gz")
        utils.copy_plus(raw_file, out_file)
        # Remove files with relative symlinks
        utils.remove_plus(os.path.join(work_dir, "results", "variants", "genome.vcf.gz"))
    return vcfutils.bgzip_and_index(out_file, items[0]["config"])

def _configure_somatic(paired, ref_file, region, out_file, tx_work_dir):
    utils.safe_makedir(tx_work_dir)
    cmd = [sys.executable, os.path.realpath(utils.which("configureStrelkaSomaticWorkflow.py"))]
    cmd += ["--referenceFasta=%s" % ref_file,
            "--callRegions=%s" % get_region_bed(region, [paired.tumor_data, paired.normal_data], out_file),
            "--runDir=%s" % tx_work_dir,
            "--normalBam=%s" % paired.normal_bam, "--tumorBam=%s" % paired.tumor_bam]
    if dd.get_coverage_interval(paired.tumor_data) not in ["genome"]:
        cmd += ["--targeted"]
    do.run(cmd, "Configure Strelka2 germline calling: %s" % paired.tumor_name)
    return os.path.join(tx_work_dir, "runWorkflow.py")

def _tumor_normal_genotypes(ref, alt, info, fname, coords):
    """Retrieve standard 0/0, 0/1, 1/1 style genotypes from INFO field.

    Normal -- NT field (ref, het, hom, conflict)
    Tumor -- SGT field
      - for SNPs specified as GG->TT for the normal and tumor diploid alleles. These
        can also represent more complex alleles in which case we set at heterozygotes
        pending longer term inclusion of genotypes in Strelka2 directly
        (https://github.com/Illumina/strelka/issues/16)
      - For indels, uses the ref, het, hom convention
    """
    known_names = set(["het", "hom", "ref", "conflict"])
    def name_to_gt(val):
        if val.lower() == "het":
            return "0/1"
        elif val.lower() == "hom":
            return "1/1"
        elif val.lower() in set(["ref", "confict"]):
            return "0/0"
        else:
            # Non-standard representations, het is our best imperfect representation
            # print(fname, coords, ref, alt, info, val)
            return "0/1"
    def alleles_to_gt(val):
        gt_indices = {gt.upper(): i for i, gt in enumerate([ref] + alt)}
        tumor_gts = [gt_indices[x.upper()] for x in val if x in gt_indices]
        if tumor_gts and val not in known_names:
            if max(tumor_gts) == 0:
                tumor_gt = "0/0"
            elif 0 in tumor_gts:
                tumor_gt = "0/%s" % min([x for x in tumor_gts if x > 0])
            else:
                tumor_gt = "%s/%s" % (min(tumor_gts), max(tumor_gts))
        else:
            tumor_gt = name_to_gt(val)
        return tumor_gt
    nt_val = [x.split("=")[-1] for x in info if x.startswith("NT=")][0]
    normal_gt = name_to_gt(nt_val)
    sgt_val = [x.split("=")[-1] for x in info if x.startswith("SGT=")]
    if not sgt_val:
        tumor_gt = "0/0"
    else:
        sgt_val = sgt_val[0].split("->")[-1]
        tumor_gt = alleles_to_gt(sgt_val)
    return tumor_gt, normal_gt

def _postprocess_somatic(in_file, paired):
    """Post-process somatic calls to provide standard output.

    - Converts SGT and NT into standard VCF GT fields
    - Replace generic TUMOR NORMAL names in VCF with sample names.
    """
    out_file = in_file.replace(".vcf.gz", "-fixed.vcf")
    if not utils.file_exists(out_file) and not utils.file_exists(out_file + ".gz"):
        with file_transaction(paired.tumor_data, out_file) as tx_out_file:
            with utils.open_gzipsafe(in_file) as in_handle:
                with open(tx_out_file, "w") as out_handle:
                    added_gt = False
                    normal_index, tumor_index = (None, None)
                    for line in in_handle:
                        if line.startswith("##FORMAT") and not added_gt:
                            added_gt = True
                            out_handle.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
                            out_handle.write(line)
                        elif line.startswith("#CHROM"):
                            assert added_gt
                            parts = line.strip().split("\t")
                            normal_index = parts.index("NORMAL")
                            tumor_index = parts.index("TUMOR")
                            line = line.replace("NORMAL", paired.normal_name).replace("TUMOR", paired.tumor_name)
                            out_handle.write(line)
                        elif line.startswith("#"):
                            out_handle.write(line)
                        else:
                            parts = line.rstrip().split("\t")
                            tumor_gt, normal_gt = _tumor_normal_genotypes(parts[3], parts[4].split(","),
                                                                          parts[7].split(";"), in_file, parts[:2])
                            parts[8] = "GT:%s" % parts[8]
                            parts[normal_index] = "%s:%s" % (normal_gt, parts[normal_index])
                            parts[tumor_index] = "%s:%s" % (tumor_gt, parts[tumor_index])
                            out_handle.write("\t".join(parts) + "\n")
    return vcfutils.bgzip_and_index(out_file, paired.tumor_data["config"])

def _run_somatic(paired, ref_file, assoc_files, region, out_file):
    if not utils.file_exists(out_file):
        work_dir = "%s-work" % utils.splitext_plus(out_file)[0]
        with file_transaction(paired.tumor_data, work_dir) as tx_work_dir:
            workflow_file = _configure_somatic(paired, ref_file, region, out_file, tx_work_dir)
            _run_workflow(paired.tumor_data, workflow_file, tx_work_dir)
        var_dir = os.path.join(work_dir, "results", "variants")
        vcfutils.combine_variant_files([_postprocess_somatic(os.path.join(var_dir, f), paired)
                                        for f in ["somatic.snvs.vcf.gz", "somatic.indels.vcf.gz"]],
                                       out_file, ref_file, paired.tumor_data["config"], region=region)
    return out_file

def _run_workflow(data, workflow_file, work_dir):
    """Run Strelka2 analysis inside prepared workflow directory.
    """
    utils.remove_safe(os.path.join(work_dir, "workspace"))
    cmd = [sys.executable, workflow_file, "-m", "local", "-j", dd.get_num_cores(data), "--quiet"]
    do.run(cmd, "Run Strelka2: %s" % dd.get_sample_name(data))
    utils.remove_safe(os.path.join(work_dir, "workspace"))
