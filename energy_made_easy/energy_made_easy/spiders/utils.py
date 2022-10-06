def get_port_number(port):
    
    port = port.replace('document.write(":"', '')
    port = port.replace(")", "")
    port = port.replace("(", "")
    port = port.replace("^", "")
    
    
    ports_elm = port.split("+")
    print(ports_elm)
    combinations = {
        "One0OneZeroOne4Eight" : "0",
        "One7NineEightTwo3Seven" : "1",
        "Seven1FourThreeFive0Five" : "2",
        "Eight8SixSixFour9Zero" : "3",
        "ZeroSevenEightFourEight2Two" : "4",
        "Four3ZeroTwoSeven4Six" : "5",
        "ZeroZeroSevenSevenEightSixFour" : "6",
        "Six9TwoOneNine7One" : "7",
        "TwoTwoThreeFiveNine8Nine" : "8",
        "One4FiveNineNineTwoThree" : "9"    
    }
    
    port = ""
    for elm in ports_elm:
        port += combinations[elm]
    
    return port
    
    