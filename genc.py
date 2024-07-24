import xml.etree.ElementTree as ET

class OpCode:
    def __init__(self, ins, operand_encodings):
        self.x32m = ins.attrib["x32m"]
        self.x64m = ins.attrib["x64m"]
        self.args = ins.find("args").text

        opc = ins.find("opc")
        if opc:
            openc = opc.attrib.get("openc")
            if openc:
                self.operand_encoding = operand_encodings[openc]

class Instruction:
    def __init__(self, common):
        self.brief = common.find("brief").text
    
        operand_encodings = {}
        for operand_encoding in common.iter("oprndenc"):
            name = operand_encoding.attrib["openc"]
            
            operands = []
            operands.append(operand_encoding.find("oprnd1").text)
            operands.append(operand_encoding.find("oprnd2").text)
            operands.append(operand_encoding.find("oprnd3").text)
            operands.append(operand_encoding.find("oprnd4").text)

            operand_encodings[name] = operands

        self.opcodes = []
        for ins in common.iter("ins"):
            self.opcodes.append(OpCode(ins, operand_encodings))


def parse_file(path):
    tree = ET.parse(path)
    root = tree.getroot()

    instructions = []
    for common in root:
        instructions.append(Instruction(common))
    
    for instruction in instructions:
        print(instruction.brief)
        print(instruction.opcodes)


if __name__ == "__main__":
    parse_file("xml/raw/x86/Intel/AZ.xml")