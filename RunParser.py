import ply
import PALParser1,PALParser2

global result2

#Open PAL model file and parse it
with open('simplePALmodel.pal', 'r')as myfile:
    model=myfile.read()
    # First Pass
    result1 = PALParser1.parse(model)
    #Second Pass
    result2 = PALParser2.parse(result1)
    print('Model Parsed :)')

#Output to parsed model in Bio-PEPA file format
with open('simplePALmodel2.biopepa', 'w') as myfile:
    myfile.write(result2)

    
    
