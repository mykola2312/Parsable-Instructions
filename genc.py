import re
import xml.etree.ElementTree as ET
from enum import Enum

class InstructionType(Enum):
    STANDARD = 0
    VEX = 1
    EVEX = 2

class Instruction:
    REX_REGEX = re.compile("^REX\\.(.)")
    BYTES_REGEX = re.compile("([0-9A-F][0-9A-F])")
    DIGIT_REGEX = re.compile("\\/(\\d)")
    MODRM_REGEX = re.compile("\\/r")
    IMM_REGEX = re.compile("i(.)")
    VALUE_REGEX = re.compile("c(.)")
    OPREG_REGEX = re.compile("r(.)")

    def parse_standard(self, opc):
        rex = Instruction.REX_REGEX.search(opc)
        bytes = Instruction.BYTES_REGEX.findall(opc)
        digit = Instruction.DIGIT_REGEX.search(opc)
        modrm = Instruction.MODRM_REGEX.search(opc)
        imm = Instruction.IMM_REGEX.search(opc)
        value = Instruction.VALUE_REGEX.search(opc)
        opreg = Instruction.OPREG_REGEX.search(opc)
        self.bytes = bytes

        self.rex = None
        self.digit = None
        self.modrm = False
        self.imm = None
        self.value = None
        self.opreg = None

        if rex: self.rex = rex.group(1)
        if digit: self.digit = int(digit.group(1))
        if modrm: self.modrm = True
        if imm: self.imm = imm.group(1)
        if value: self.value = value.group(1)
        if opreg: self.opreg = opreg.group(1)

        self.has_modrm = self.modrm or self.digit is not None

    def parse_vex(self, opc):
        pass

    def parse_evex(self, opc):
        raise NotImplemented("EVEX is not implemented")

    def __init__(self, ins):
        self.x32m = ins.attrib["x32m"]
        self.x64m = ins.attrib["x64m"]
        self.mnemonic = ins.find("mnem").text
        
        opc = ins.find("opc").text
        if "EVEX" in opc:
            self.type = InstructionType.EVEX
            self.parse_evex(opc)
        elif "VEX" in opc:
            self.type = InstructionType.VEX
            self.parse_vex(opc)
        else:
            self.type = InstructionType.STANDARD
            self.parse_standard(opc)

        print(self)
    
    def __str__(self):
        return f"{self.mnemonic} rex {self.rex} bytes {self.bytes} has_modrm {self.has_modrm} digit {self.digit} modrm {self.modrm} imm {self.imm} value {self.value} opreg {self.opreg}"

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