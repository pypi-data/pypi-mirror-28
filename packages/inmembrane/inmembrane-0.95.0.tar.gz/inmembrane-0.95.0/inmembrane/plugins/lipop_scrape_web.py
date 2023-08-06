# -*- coding: utf-8 -*-
citation = {'ref': u"Agnieszka S. Juncker, Hanni Willenbrock, "
                   u"Gunnar Von Heijne, Søren Brunak, Henrik Nielsen, "
                   u"And Anders Krogh. (2003) Prediction of lipoprotein "
                   u"signal peptides in Gram-negative bacteria. Protein "
                   u"Science 12:1652–1662. \n"
                   u"<http://dx.doi.org/10.1110/ps.0303703>",
            'name': "LipoP 1.0 (web interface)"
            }

__DEBUG__ = False

import sys, os, time
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup
import requests

try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict

import inmembrane
from inmembrane.plugins.lipop1 import parse_lipop
from inmembrane.helpers import log_stderr
from inmembrane.helpers import generate_safe_seqids, proteins_to_fasta


def annotate(params, proteins, batchsize=2000, force=False):
    """
    This plugin interfaces with the LipoP web interface (for humans) and
    scrapes the results. There once was a SOAP service but it was discontinued,
    so now we use this.
    """

    baseurl = "http://www.cbs.dtu.dk"
    url = baseurl + "/cgi-bin/webface2.fcgi"

    # grab the cached results if present
    outfile = "lipop_scrape_web.out"
    if not force and os.path.isfile(outfile):
        log_stderr("# -> skipped: %s already exists" % outfile)
        proteins, id_mapping = generate_safe_seqids(proteins)
        fh = open(outfile, 'r')
        resultpage = fh.read()
        fh.close()
        # soup = BeautifulSoup(resultpage)
        proteins = parse_lipop(resultpage, proteins, id_mapping=id_mapping)
        return proteins

    proteins, id_mapping = generate_safe_seqids(proteins)

    seqids = proteins.keys()
    allresultpages = ""
    while seqids:
        seqid_batch = seqids[0:batchsize]
        del seqids[0:batchsize]

        # get batch of sequences in fasta format with munged ids
        # (workaround for lipop sequence id munging)
        safe_fasta = proteins_to_fasta(proteins,
                                       seqids=seqid_batch,
                                       use_safe_seqid=True)

        # we use an OrderedDict rather than a normal dictionary to work around
        # some quirks in the CBS CGI (the server expects parameters in a certain
        # order in the HTTP headers).
        payload = OrderedDict([('configfile',
                                "/usr/opt/www/pub/CBS/services/LipoP-1.0/LipoP.cf"),
                               ("SEQ", ""),
                               ("outform", "-noplot")])

        # files = {'seqfile': open(params['fasta'], 'rb')}
        files = {'SEQSUB': StringIO(safe_fasta)}

        log_stderr("# LipoP(scrape_web), %s > %s" % (params['fasta'], outfile))

        headers = {"User-Agent":
                       "python-requests/%s (inmembrane/%s)" %
                       (requests.__version__, inmembrane.__version__)}
        r_post = requests.post(url, data=payload, files=files, headers=headers)

        if __DEBUG__:
            log_stderr(r_post.text)
            # Example:
            #
            # <HTML>
            # <HEAD><TITLE>Webface Jobsubmission</TITLE></HEAD>
            # If Javascript is disabled, follow <a href="/cgi-bin/webface?jobid=LipoP,50B5432A10A9CD51&opt=wait">This link</a>
            #
            # <script LANGUAGE="JavaScript"><!--
            # location.replace("/cgi-bin/webface?jobid=LipoP,50B5432A10A9CD51&opt=wait")
            # //--></script>
            # </HTML>

        # extract the result URL (or die if job is rejected ...)
        if "Job rejected" in r_post.text:
            log_stderr(r_post.text)
            sys.exit()

        r_post_clean = r_post.text.replace("<noscript>", "").replace(
            "</noscript", "")
        soup = BeautifulSoup(r_post_clean)
        pollingurl = soup.findAll('a')[0]['href']
        sys.stderr.write("# Fetching from: " + pollingurl + "\n");
        # try grabbing the result, then keep polling until they are ready
        sys.stderr.write("# Waiting for LipoP(scrape_web) results ")
        waittime = 1.0
        time.sleep(waittime)  # (len(proteins)/500)
        resultpage = requests.get(pollingurl).text
        retries = 0
        while (("<title>Job status of" in resultpage) and (retries < 15)):
            sys.stderr.write(".")
            time.sleep(waittime)  # (len(proteins)/500)
            resultpage = requests.get(pollingurl).text
            waittime += 1;
            retries += 1
            waittime = min(waittime, 20)

        sys.stderr.write(" .. done !\n")

        if __DEBUG__:
            log_stderr(resultpage)
            # Example:
            #
            #   <pre>
            # # lcl_AE004092.1_cdsid_AAK33146.1 CYT score=-0.200913
            # # Cut-off=-3
            # lcl_AE004092.1_cdsid_AAK33146.1	LipoP1.0:Best	CYT	1	1	-0.200913
            # <P>
            # <hr>
            # # lcl_AE004092.1_cdsid_AAK33147.1 CYT score=-0.200913
            # # Cut-off=-3
            # lcl_AE004092.1_cdsid_AAK33147.1	LipoP1.0:Best	CYT	1	1	-0.200913
            # <P>
            # <hr>

        allresultpages += clean_result_page(resultpage)

    # we store the cleaned up result pages concatenated together
    fh = open(outfile, 'a+')
    fh.write(allresultpages)
    fh.close()

    proteins = parse_lipop(allresultpages, proteins, id_mapping=id_mapping)
    return proteins


# TODO: Consider using helpers.html2text instead
def clean_result_page(resultpage):
    """
    Takes the HTML output from the LipoP result page and replaces some
    tags make the output parsable by the existing standalone lipop1 parser.
    """
    resultpage = "\n".join(resultpage.split('\n')[14:])
    resultpage = resultpage.replace("<hr>", '\n')
    resultpage = resultpage.replace("<P>", '')
    resultpage = resultpage.replace("<pre>", '')
    resultpage = resultpage.replace("</pre>", '')
    return resultpage
