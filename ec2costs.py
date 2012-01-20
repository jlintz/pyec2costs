#!/usr/bin/env python
import json
import urllib2

ondemand_costs_url = "http://aws.amazon.com/ec2/pricing/pricing-on-demand-instances.json"
reserved_costs_url = "http://aws.amazon.com/ec2/pricing/pricing-reserved-instances.json"

ec2_type_map = {"stdODI": "m1",
                "uODI": "t1",
                "hiMemODI": "m2",
                "hiCPUODI": "c1",
                "clusterComputeI": "cc1",
                "clusterGPUI": "cg1"}

ec2_size_map = {"sm": "small",
                "lg": "large",
                "xl": "xlarge",
                "u": "micro",
                "xxl": "2xlarge",
                "xxxxl": "4xlarge",
                "med": "medium",
                "xxxxxxxxl": "8xlarge"}

ec2_region_map = {"apac-sin": "ap-northeast-1",
                "us-west": "us-west-1",
                "eu-ireland": "eu-west-1",
                "apac-tokyo": "ap-southeast-1",
                "us-east": "us-east-1",
                "us-west-2": "us-west-2",
                "sa-east-1": "sa-east-1"}


def get_current_ondemand_costs():
    prices = {}
    data = json.loads(urllib2.urlopen(ondemand_costs_url).read())

    for region in data["config"]["regions"]:
        region = dict(region)
        prices[ec2_region_map[region["region"]]] = {}
        for instance in region["instanceTypes"]:
            inst_type = instance["type"]
            for size in instance["sizes"]:
                for values in size["valueColumns"]:
                    if values["name"] == "linux":
                        linux_cost = values["prices"]["USD"]
                    elif values["name"] == "mswin":
                        win_cost = values["prices"]["USD"]
                prices[ec2_region_map[region["region"]]][ec2_type_map[inst_type] + "." + ec2_size_map[size["size"]]] = {"windows": win_cost, "linux": linux_cost}

    return prices

def get_current_reserved_costs():
    print "Implement"

if __name__ == "__main__":
   print get_current_ondemand_costs() 
