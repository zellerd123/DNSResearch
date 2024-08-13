from argparse import ArgumentParser
from scripts import (
    NameserverResolver, 
    IPResolver, 
    ASNResolver, 
    AS_ORG_Resolver, 
    ResultProcessor,
    ResultPresenter
)
import os
import time

def main():
    def gather_nameservers():
        start = time.time()
        print('Begin Step 1: Executing Nameserver Resolution')
        nameserver_resolver = NameserverResolver(settings.records, settings.max_threads)
        failed_resolutions = nameserver_resolver.execute_nameserver_resolution()
        print(f'Completed Step 1 - Total Time: {time.time()-start} seconds. Failed NS Resolutions: {failed_resolutions}')

    def gather_ips():
        start = time.time()
        print('Begin Step 2: Executing IP Resolution for Nameservers')
        ip_resolver = IPResolver(settings.max_threads)
        failed_resolutions = ip_resolver.execute_ip_resolution()
        print(f'Completed Step 2: - Total Time: {time.time()-start} seconds. Failed A Resolutions: {failed_resolutions}')

    def gather_asns():
        start = time.time()
        print('Begin Step 3: Executing ASN Resolution for IPs')
        asn_resolver = ASNResolver(settings.max_threads)
        failed_resolutions = asn_resolver.execute_asn_resolution()
        print(f'Completed Step 3 - Total Time: {time.time()-start} seconds. Failed TXT Resolutions: {failed_resolutions}')

    def gather_as_orgs():
        start = time.time()
        print('Begin Step 4: Executing AS Org Resolution for ASNs')
        as_org_resolver = AS_ORG_Resolver(settings.max_threads)
        failed_resolutions = as_org_resolver.execute_as_org_resolution()
        print(f'Completed Step 4 - Total Time: {time.time()-start} seconds. Failed TXT Resolutions: {failed_resolutions}')

    def process_results():
        print('Data Collection Complete. Processing Data and creating graphics.')
        result_processor = ResultProcessor()
        result_processor.execute_process_all_results()

    def present_results():
        result_presenter = ResultPresenter()
        result_presenter.create_bar_chart()
        result_presenter.create_table()
        result_presenter.create_inbailwick_table()

    start_overall = time.time()
    arg_parser = ArgumentParser(description='Messenger', add_help=False)

    arg_parser.add_argument('-r', '--records', dest='records', 
            action='store', type=int, default=10000,
            help='''Number of Tranco Records to use''')
    arg_parser.add_argument('-t', '--threads', dest='max_threads',
            action='store', type=int, default=25, 
            help='''Maximum number of threads to spawn for DNS Resolutions''')
    settings = arg_parser.parse_args()

    gather_nameservers()
    gather_ips()
    gather_asns()
    gather_as_orgs()
    process_results()
    present_results()
    print(f'Total time to run entire research: {time.time()-start_overall} seconds')


if __name__ == '__main__':
    main()