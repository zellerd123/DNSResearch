from scripts import DNSResolver, ThreadPoolExecutor, json

'''
STEP 3.5 OF RESEARCH
Convert ASN -> Organization Name
'''
class AS_ORG_Resolver(DNSResolver):
    def __init__(self, max_threads : int = 25):
        super().__init__(record_type = 'TXT')
        self._max_threads = max_threads

    
    def asn_to_query(self, asn: str):
        '''
        Turns an ASN into a valid Organization Name query for team-cymru
        
        @Keyword arguments: 
        asn(str): ASN to be converted into query format 
        '''
        query = f'AS{asn}.asn.cymru.com'
        return query
    
    
    def clean_for_organization(self, response : str):
        '''
        Cleans ASN --> Org Name Query
        
        @Keyword arguments:
        response(str): The raw response string from ASN to Org name query
        '''
        return response.split(' | ')[-1].strip('"')

    
    def execute_as_org_resolution(self):
        '''Executes ASN Resolution from results of IP Resolution'''
        # Get IP to List[ASN] mapping.
        ip_to_asn : Dict[str, List[str]] = self.read_json('outputs/ip_to_asn_mapping.json')

        # Get all unique ASNs from the IP to ASN mapping.
        all_asns = [asn for asn_list in ip_to_asn.values() for asn in asn_list]
        unique_asns = set(all_asns)

        # Get mapping of ASN to Organization Name.
        asn_queries = [self.asn_to_query(asn) for asn in unique_asns]
        with ThreadPoolExecutor(max_workers=self._max_threads) as executor:
            org_results = list(executor.map(self.resolve, asn_queries))
        asn_to_org = {asn: self.clean_for_organization(response) for asn, response in zip(unique_asns, org_results)}

        # Store ASN to Organization Name mapping in its own JSON.
        with open('outputs/asn_to_org_mapping.json', 'w') as jsonfile:
            json.dump(asn_to_org, jsonfile, indent=4)

        return self._resolution_failed_counter