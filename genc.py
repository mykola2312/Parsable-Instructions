import re
import xml.etree.ElementTree as ET

class OpCode:
    OPCODE_REGEX = re.compile("[0-9A-F][0-9A-F]")

    def __init__(self, ins, operand_encodings):
        self.x32m = ins.attrib["x32m"]
        self.x64m = ins.attrib["x64m"]
        self.args = ins.find("args").text

        opc = ins.find("opc")
        self.opcode = OpCode.OPCODE_REGEX.findall(opc.text)

        openc = opc.attrib.get("openc")
        if openc:
            self.operand_encoding = operand_encodings.get(openc, openc)
        else: self.operand_encoding = None
    
    def __str__(self):
        return f"\topcode {self.opcode} args {self.args} op_enc {self.operand_encoding}"

class Instruction:
    SKIP_16BIT_REALMODE = ["rel16", "ptr16:16"]


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
        
        # remove 16 bit real mode displacement value opcodes
        self.opcodes = list(filter(lambda op: op.args not in Instruction.SKIP_16BIT_REALMODE, self.opcodes))


def parse_file(path):
    tree = ET.parse(path)
    root = tree.getroot()

    instructions = []
    for common in root:
        instructions.append(Instruction(common))
    
    for instruction in instructions:
        print(instruction.brief)
        for opcode in instruction.opcodes:
            print(opcode)


if __name__ == "__main__":
    parse_file("xml/raw/x86/Intel/AZ.xml")