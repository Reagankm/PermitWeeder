import json
import re

def main():

    all_permits = []
    good_permits = []
    counter = 0
    out_file = open('output.json', 'w')

    ## Read all the permit data and save it in condensed form
    with open('hackcessible-webapp/static/data/sdot-sidewalk-closed-by-address.json') as data_file:
        contents = json.load(data_file)
        data = contents["data"]
        for i in range(len(data)):
            permit = data[i]
            shapeArray = permit[9]
            lat_lng = [shapeArray[1], shapeArray[2]] 
            description = permit[24] 
            mobility_impact = permit[16] 
            address = permit[20]
            sidewalk_closed = permit[34]
            closure_start = permit[35]
            closure_end = permit[36]
            sidewalk_blocked = permit[40]
            if (sidewalk_blocked != None):
                print("swalk blocked: " + sidewalk_blocked)
            block_start = permit[41]
            block_end = permit[42]
            
            site = {'lat_lng' : lat_lng, 'address' : address,
                    'mobility_impact' : mobility_impact,
                    'description' : description,
                    'sidewalk_closed': sidewalk_closed,
                    'closure_start': closure_start,
                    'closure_end': closure_end,
                    'sidewalk_blocked': sidewalk_blocked,
                    'block_start': block_start,
                    'block_end': block_end
            }
            all_permits.append(site)
   
    for p in all_permits:
        #Check for right of way impact
        mobImp = p['mobility_impact']
        if (mobImp != None and mobImp != "4-No ROW Blockage") or mobImp == None:
            desc = p['description']
            end = p['closure_end']
            start = p['closure_start']
            if ((desc != None and desc.find("NO MOBILITY IMPACT") == -1 and desc.find("FOOD TRUCK") == -1 and desc.find("VENDING") == -1 and desc.find("PLUM BURGER") == -1 and desc.find("FALAFEL SAM") == -1 and  desc.find("RANEY BROTHERS BBQ") == -1 and desc.find("CHOPSTIX") == -1 and desc.find("CONTIGO") == -1 and desc.find("DJUNG ON WHEELS") == -1 and desc.find("WICKED PIES") == -1 and desc.find("FUSION ON THE RUN") == -1 and desc.find("STREET TREATS") == -1 and desc.find("BUNS ON WHEELS") == -1 and desc.find("HUNGRY ME") == -1 and desc.find("LUMPIA WORLD") == -1 and desc.find("JEMILS BIG EASY") == -1) or desc == None) and ((p['sidewalk_closed'] == "Y" and end > 1430269961 and start < 1430269961) or(p['sidewalk_blocked'] == "Y" and p['block_start'] <1430269961 and p['block_end']>1430269961 )):
                #Check to see if it's already expired per description text
                #expiration_patt = re.compile(".*?EXPIRES:?[\s]*([0-9][0-9]?)/([0-9][0-9]?)/((20)?[0-9][0-9]).*?", re.IGNORECASE)
                #match = expiration_patt.match(desc)
                #if match:
                    #print(desc)
                    
                
                good_permits.append(p)
                #if ("EXPIRES" in desc):
                #    print(desc + "\n")
                #counter += 1
                
    json.dump(good_permits, out_file)
            
            
            
            


main()
