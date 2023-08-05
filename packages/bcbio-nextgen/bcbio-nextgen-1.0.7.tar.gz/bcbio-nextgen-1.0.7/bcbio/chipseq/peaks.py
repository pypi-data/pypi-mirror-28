"""High level parallel chip-seq analysis
"""
import os
import copy
import toolz as tz

import subprocess

from bcbio.log import logger
from bcbio import utils
from bcbio.pipeline import config_utils
from bcbio.pipeline import datadict as dd
from bcbio.provenance import do
from bcbio.distributed.transaction import file_transaction


def get_callers():
    """Get functions related to each caller"""
    from bcbio.chipseq import macs2
    return {"macs2": macs2.run}

def peakcall_prepare(data, run_parallel):
    """Entry point for doing peak calling"""
    caller_fns = get_callers()
    to_process = []
    for sample in data:
        mimic = copy.copy(sample[0])
        callers = dd.get_peakcaller(sample[0])
        if not isinstance(callers, list):
            callers = [callers]
        for caller in callers:
            if caller in caller_fns:
                mimic["peak_fn"] = caller
                name = dd.get_sample_name(mimic)
                mimic = _check(mimic, data)
                if mimic:
                    to_process.append(mimic)
                else:
                    logger.info("Skipping peak calling. No input sample for %s" % name)
    if to_process:
        after_process = run_parallel("peakcalling", to_process)
        data = _sync(data, after_process)
    return data

def calling(data):
    """Main function to parallelize peak calling."""
    chip_bam = dd.get_work_bam(data)
    input_bam = data.get("work_bam_input", None)
    caller_fn = get_callers()[data["peak_fn"]]
    name = dd.get_sample_name(data)
    out_dir = utils.safe_makedir(os.path.join(dd.get_work_dir(data), data["peak_fn"], name))
    encode_bed = tz.get_in(["genome_resources", "variation", "encode_blacklist"], data)
    # lcr_bed = utils.get_in(data, ("genome_resources", "variation", "lcr"))
    if encode_bed:
        chip_bam = _prepare_bam(chip_bam, encode_bed, data['config'])
        data["work_bam_filter"] = chip_bam
        input_bam = _prepare_bam(input_bam, encode_bed, data['config'])
        data["input_bam_filter"] = input_bam
    out_files = caller_fn(name, chip_bam, input_bam, dd.get_genome_build(data), out_dir,
                          dd.get_chip_method(data), data["resources"], data["config"])
    greylistdir = greylisting(data)
    data.update({"peaks_files": out_files})
    if greylistdir:
        data["greylist"] = greylistdir
    return [[data]]
    data["input_bam_filter"] = input_bam

def _prepare_bam(bam_file, bed_file, config):
    """Remove regions from bed files"""
    if not bam_file or not bed_file:
        return bam_file
    out_file = utils.append_stem(bam_file, '_filter')
    bedtools = config_utils.get_program("bedtools", config)
    if not utils.file_exists(out_file):
        with file_transaction(out_file) as tx_out:
            cmd = "{bedtools} subtract -nonamecheck -A -a {bam_file} -b {bed_file} > {tx_out}"
            do.run(cmd.format(**locals()), "Clean %s" % bam_file)
    return out_file

def _sync(original, processed):
    """
    Add output to data if run sucessfully.
    For now only macs2 is available, so no need
    to consider multiple callers.
    """
    for original_sample in original:
        original_sample[0]["peaks_files"] = {}
        for process_sample in processed:
            if dd.get_sample_name(original_sample[0]) == dd.get_sample_name(process_sample[0]):
                for key in ["peaks_file", "work_bam_filter", "input_bam_filter"]:
                    if process_sample[0].get(key):
                        original_sample[0][key] = process_sample[0][key]
    return original

def _check(sample, data):
    """Get input sample for each chip bam file."""
    if dd.get_chip_method(sample).lower() == "atac":
        return [sample]
    if dd.get_phenotype(sample) == "input":
        return None
    for origin in data:
        if dd.get_batch(sample) in (dd.get_batches(origin[0]) or []) and dd.get_phenotype(origin[0]) == "input":
            sample["work_bam_input"] = dd.get_work_bam(origin[0])
            return [sample]
    return [sample]

def _get_multiplier(samples):
    """Get multiplier to get jobs
       only for samples that have input
    """
    to_process = 1.0
    to_skip = 0
    for sample in samples:
        if dd.get_phenotype(sample[0]) == "chip":
            to_process += 1.0
        elif dd.get_chip_method(sample[0]).lower() == "atac":
            to_process += 1.0
        else:
            to_skip += 1.0
    mult = (to_process - to_skip) / len(samples)
    if mult <= 0:
        mult = 1 / len(samples)
    return max(mult, 1)

def greylisting(data):
    """
    Run ChIP-seq greylisting
    """
    input_bam = data.get("work_bam_input", None)
    if not input_bam:
        logger.info("No input BAM file detected, skipping greylisting.")
        return None
    try:
        greylister = config_utils.get_program("chipseq-greylist", data)
    except config_utils.CmdNotFound:
        logger.info("No greylister found, skipping greylisting.")
        return None
    greylistdir = os.path.join(os.path.dirname(input_bam), "greylist")
    if os.path.exists(greylistdir):
        return greylistdir
    cmd = "{greylister} --outdir {txgreylistdir} {input_bam}"
    message = "Running greylisting on %s." % input_bam
    with file_transaction(greylistdir) as txgreylistdir:
        utils.safe_makedir(txgreylistdir)
        try:
            do.run(cmd.format(**locals()), message)
        except subprocess.CalledProcessError as msg:
            if str(msg).find("Cannot take a larger sample than population when 'replace=False'") >= 0:
                logger.info("Skipping chipseq greylisting because of small sample size: %s"
                            % dd.get_sample_name(data))
                return None
    return greylistdir
