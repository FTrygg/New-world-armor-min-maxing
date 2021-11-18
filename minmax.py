
import copy
import os


light_threshold = 13
medium_threshold = 23

helmets = [{"weightclass" : "L","weight" : 1.5, "protection" : 72.1 },{"weightclass" : "M","weight" : 2.6, "protection" : 128 },{"weightclass" : "H","weight" : 4.7, "protection" : 227 }]#
chests = [{"weightclass" : "L","weight" : 3.5, "protection" : 168.2 },{"weightclass" : "M","weight" : 6.2, "protection" : 298 },{"weightclass" : "H","weight" : 11, "protection" : 529.8 }]#
gloves = [{"weightclass" : "L","weight" : 1.5, "protection" : 72.1 },{"weightclass" : "M","weight" : 2.6, "protection" : 128 },{"weightclass" : "H","weight" : 4.7, "protection" : 227 }]#
pants = [{"weightclass" : "L","weight" : 2, "protection" : 96.1 },{"weightclass" : "M","weight" : 3.5, "protection" : 170.6 },{"weightclass" : "H","weight" : 6.3, "protection" : 302.7 }]#
boots = [{"weightclass" : "L","weight" : 1.5, "protection" : 72.1 },{"weightclass" : "M","weight" : 2.6, "protection" : 128 },{"weightclass" : "H","weight" : 4.7, "protection" : 227 }]#


def minmax() -> list:
    combinations = []

    for h in helmets:
        combinations.append([h])
    
    branch(combinations,chests)
    branch(combinations,gloves)
    branch(combinations,pants)
    branch(combinations,boots)
    
    return combinations
    
def branch(combinations : list, amroritem : list) -> None:
    newcombos = []
    for com in combinations:
        root = copy.deepcopy(com)
        for index, c in enumerate(amroritem):
            if index == 0:
                com.append(c)
            else:
                newbranch = copy.deepcopy(root)
                newbranch.append(c)
                newcombos.append(newbranch)
    combinations.extend(newcombos)

def evaluate(all_combinations : list) -> None:
    valid_med = []
    valid_light = []
    for combo in minmax():
        combined_weight = 0
        combined_protection = 0
        weightclasses = []
        for item in combo:
            combined_weight += item["weight"]
            combined_protection += item["protection"]
            weightclasses.append(item["weightclass"])

        line = {"weight" : round(combined_weight,2), "protection" : round(combined_protection,2), "wcombo" : weightclasses}


        if combined_weight <= medium_threshold:
            valid_med.append(line)

        if combined_weight <= light_threshold:
            valid_light.append(line)

    light = sorted(valid_light, key=lambda d: d['protection'], reverse=True) 
    medium = sorted(valid_med, key=lambda d: d['protection'], reverse=True) 

    writeToCsv("medium",medium)
    writeToCsv("light",light)

def writeToCsv(targetweight : str, sortedCombos : list) -> None:
    filename = "Min-maxed_" + targetweight + ".csv"
    cwd = os.path.dirname(__file__)
    abspath = os.path.join(cwd,filename)
    with open(abspath,"w+") as f:
        f.write("Rank; Total weight; Total protection; Helmet weightclass; Chests weightclass; Gloves weightclass; Pants weightclass; Boots weightclass;\n")
        for index, comb in enumerate(sortedCombos):
            w = comb["weight"]
            p = comb["protection"]

            row = "{0};{1};{2};".format(index+1,w,p)
            for i in comb["wcombo"]:
                row = row + i + ";"
            
            row = row +"\n"
            f.write(row)

        f.write("\nLight = L\n") 
        f.write("Medium = M\n") 
        f.write("Heavy = H\n") 
    
s = minmax()
evaluate(s)






