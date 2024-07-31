import re
import xml.etree.ElementTree as ET

class Instruction:
    REX_REGEX = re.compile("^REX\\.(.)")
    BYTES_REGEX = re.compile("([0-9A-F][0-9A-F])")
    DIGIT_REGEX = re.compile("\\/(\\d)")
    MODRM_REGEX = re.compile("\\/r")
    IMM_REGEX = re.compile("i(.)")
    VALUE_REGEX = re.compile("c(.)")
    OPREG_REGEX = re.compile("r(.)")

    def __init__(self, ins):
        self.x32m = ins.attrib["x32m"]
        self.x64m = ins.attrib["x64m"]
        
        opc = ins.find("opc").text
        if "VEX" in opc: return

        rex = Instruction.REX_REGEX.search(opc)
        bytes = Instruction.BYTES_REGEX.findall(opc)
        digit = Instruction.DIGIT_REGEX.search(opc)
        modrm = Instruction.MODRM_REGEX.search(opc)
        imm = Instruction.IMM_REGEX.search(opc)
        value = Instruction.VALUE_REGEX.search(opc)
        opreg = Instruction.OPREG_REGEX.search(opc)

        print(ins.find("mnem").text)
        if rex: print("rex\t", rex.group(1))
        print(bytes)
        if digit: print("digit\t", digit.group(1))
        if modrm: print("modrm\t", modrm.group(0))
        if imm: print("imm\t", imm.group(1))
        if value: print("value\t", value.group(1))
        if opreg: print("opreg\t", opreg.group(1))

class InstructionGroup:
    def __init__(self, common):
        self.brief = common.find("brief").text
        self.instructions = [Instruction(ins) for ins in common.iter("ins")]


def parse_file(path):
    tree = ET.parse(path)
    root = tree.getroot()

    groups = [InstructionGroup(common) for common in root.iter("common")]
    return groups


if __name__ == "__main__":
    parse_file("xml/raw/x86/Intel/AZ.xml")