from scripts import DNSResolver, ThreadPoolExecutor, json

'''
STEP 3 OF RESEARCH
Convert IP Address -> Autonomous System Number
'''
class ASNResolver(DNSResolver):
    def __init__(self, max_threads : int = 25):
        super().__init__(record_type = 'TXT')
        self._max_threads = max_threads

    
    def ip_to_query(self, ip : str):
        '''
        Turns IP into a valid ASN query for team-cymru
        
        @Keyword arguments: 
        ip(str): the IP address to be converted into ASN query format
        '''
        query = '.'.join(reversed(ip.split('.'))) + '.origin.asn.cymru.com'
        return query

    
    def clean_for_asn_number(self, response: str):
        '''
        Cleans ip->asn query
        
        @Keyword arguments:
        response(str): The raw response string from IP to ASN query
        '''
        return response.split(' | ')[0].strip('"').split()

    
    def execute_asn_resolution(self):
        '''Executes ASN Resolution from results of IP Resolution'''
        ips : List[str] = list(self.read_json(output_file_name = 'outputs/nameserver_ips.json').values())
        ip_queries = [self.ip_to_query(ip) for ip in ips]

        # create thread pool executor to resolve asn of each ip
        with ThreadPoolExecutor(max_workers=self._max_threads) as executor:
            results = list(executor.map(self.resolve, ip_queries))

        # Clean results of ASN resolution from nameservers.
        cleaned_results = self.drop_failed_resolutions(zip(ips, results))

        # Create a dictionary from the cleaned results
        ip_to_asn = {ip: self.clean_for_asn_number(response) for ip, response in cleaned_results}

        # Store IP to List[ASN] mapping in its own JSON.
        with open('outputs/ip_to_asn_mapping.json', 'w') as jsonfile:
            json.dump(ip_to_asn, jsonfile, indent=4)

        return self._resolution_failed_counter