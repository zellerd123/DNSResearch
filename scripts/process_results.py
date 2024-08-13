from typing import List, Dict, Tuple
import json

class ResultProcessor():
    def __init__(self):
        # Prep JSON
        self._domains_to_nameservers : Dict[str, List[str]] = self.__read_json('outputs/domains_nameservers.json')
        self._nameservers_to_ips : Dict[str, str] = self.__read_json('outputs/nameserver_ips.json')
        self._ips_to_asns : Dict[str, List[str]] = self.__read_json('outputs/ip_to_asn_mapping.json')
        self._asns_to_org : Dict[str, str] = self.__read_json('outputs/asn_to_org_mapping.json')

        # Store total # of domains
        self._total_domains = len(self._domains_to_nameservers)

        # Prep storage variables
        self._unreachable_organizations, self._affected_organizations = self.__process_results_unreachable()
        self._inbailwick_domains, self._inbailwick_partial_domains = self.__process_results_inbailwick()
   
    
    def __read_json(self, file_name: str) -> Dict:
        '''
        Private function to read json
        
        @Keyword arguments:
        file_name(str): Name of requested file to unpack
        '''
        with open(file_name, 'r') as jsonfile:
            data = json.load(jsonfile)
        return data

    
    def __process_results_unreachable(self) -> Dict[str, int]:
        '''
        Private function to analyze data and returns Dictionary of 
        Organization Name -> # Full-Controlled Domains in Top 10k
        '''
        unreachable_organizations : Dict[str, int] = {}
        affected_organizations : Dict[str, int] = {}
        for domain, nameservers in self._domains_to_nameservers.items():
            # create 'set' of organizations that the domain is reliant on for hosting its nameservers
            organizations = set()
            # iterate over all nameservers for that domain
            for nameserver in nameservers:
                # get corresponding IP
                nameserver_ip = self._nameservers_to_ips.get(nameserver, None)
                if nameserver_ip == None:
                    continue
                # get corresponding asns
                asns = self._ips_to_asns.get(nameserver_ip, None)
                if asns == None:
                    continue
                # in the event its a multi-org ASN
                for asn in asns:
                    organization = self._asns_to_org.get(asn, None)
                    if organization == None:
                        continue
                    # add organization to set
                    organizations.add(organization)
            # if its only the one organization running all of the domains nameservers, add it to unreachable orgs dictionary
            if len(organizations) == 1:
                for org in organizations:
                    unreachable_organizations[org] = unreachable_organizations.get(org, 0) + 1
            for org in organizations:
                affected_organizations[org] = affected_organizations.get(org, 0) + 1
        return unreachable_organizations, affected_organizations
    
    
    def __process_results_inbailwick(self) -> List[str]:
        '''
        Private function to analyze data and returns List of 
        Domains whose Nameservers are exclusively in-bailiwick
        '''
        inbailwick_domains : List[str] = []
        inbailwick_partial_domains : List[str] = []
        for domain, nameservers in self._domains_to_nameservers.items():
            inbailwick_count = 0
            for nameserver in nameservers:
                if domain in nameserver:
                    inbailwick_count += 1
            # captures full inbailwick for all nameservers
            if inbailwick_count == len(nameservers):
                inbailwick_domains.append(domain)
            # captures partial inbailwick
            elif inbailwick_count > 0:
                inbailwick_partial_domains.append(domain)
        return inbailwick_domains, inbailwick_partial_domains

    
    def get_top_unreachable_as_numbers(self) -> List[Tuple[str, int]]:
        '''Gets Top 10 Unreachable Organizations and corresponding # of Top 10k controlled'''
        top_10_unreachable_organizations = sorted(
            self._unreachable_organizations.items(), key= lambda x: x[1], reverse=True
        )[:10]
        return top_10_unreachable_organizations

    
    def get_top_unreachable_as_percents(self) -> List[Tuple[str, float]]:
        '''Gets Top 10 Unreachable Organizations as percentages'''
        top_10_unreachable_organizations = self.get_top_unreachable_as_numbers()
        # Convert those to unreachable orgs to percents
        top_10_unreachable_percents = [
            (org, round((count / self._total_domains) * 100, 1)) for org, count in top_10_unreachable_organizations
        ]
        return top_10_unreachable_percents

    
    def get_top_affected_as_numbers(self) -> List[Tuple[str, int]]:
        '''Gets Top 10 Affected Organizations and corresponding # of Top 10k controlled'''
        top_affected = []
        top_unreachable = self.get_top_unreachable_as_numbers()
        for org, _ in top_unreachable:
            top_affected.append((org, self._affected_organizations[org]))
        return top_affected
    
    
    def get_top_affected_as_percents(self) -> List[Tuple[str, float]]:
        '''Gets Top 10 Affected Organizations as percentages'''
        top_10_affected_organizations = self.get_top_affected_as_numbers()
        # Convert those to unreachable orgs to percents
        top_10_affected_percents = [
            (org, round((count / self._total_domains) * 100, 1)) for org, count in top_10_affected_organizations
        ]
        return top_10_affected_percents

    
    def get_inbailwick_percent(self) -> float:
        '''Gets Percentage of Inbailwick Domains'''
        return round((len(self._inbailwick_domains)/self._total_domains)*100, 2)

    
    def get_inbailwick_partial_percent(self) -> float:
        '''Gets Percentage of Partial Inbailwick Domains'''
        return round((len(self._inbailwick_partial_domains)/self._total_domains)*100, 2)

    
    def execute_process_all_results(self):
        '''Processes all results'''
        # Obtain the results
        inbailwick_percent = self.get_inbailwick_percent()
        inbailwick_partial_percent = self.get_inbailwick_partial_percent()
        top_unreachable_percents = self.get_top_unreachable_as_percents()
        top_unreachable_numbers = self.get_top_unreachable_as_numbers()
        top_affected_percents = self.get_top_affected_as_percents()
        top_affected_numbers = self.get_top_affected_as_numbers()

        # Organize the results into a dictionary
        results_to_write = {
            "inbailwick_result": inbailwick_percent,
            "inbailwick_partial_percent": inbailwick_partial_percent,
            "top_unreachable_percents": top_unreachable_percents,
            "top_unreachable_numbers": top_unreachable_numbers,
            "top_affected_percents" : top_affected_percents,
            "top_affected_numbers" : top_affected_numbers
        }

        # Write the results dictionary to a JSON file
        with open('outputs/results.json', 'w') as json_file:
            json.dump(results_to_write, json_file, indent=4)


