import re
import xml.etree.ElementTree as ET
from enum import Enum

class InstructionType(Enum):
    STANDARD = 0
    VEX = 1
    EVEX = 2

class Instruction:
    def __init__(self, ins):
        self._opc = ins.find("opc").text
        self.x32m = ins.attrib["x32m"]
        self.x64m = ins.attrib["x64m"]
        self.mnemonic = ins.find("mnem").text
        
        self.bytes = None

    def get_type(self):
        pass
    
    def has_modrm(self):
        pass

    def __str__(self):
        return f"{self.mnemonic} rex {self.rex} bytes {self.bytes} has_modrm {self.has_modrm()}"

class InstructionCommon:
    REX_REGEX = re.compile("^REX\\.(.)")
    BYTES_REGEX = re.compile("([0-9A-F][0-9A-F])")
    DIGIT_REGEX = re.compile("\\/(\\d)")
    MODRM_REGEX = re.compile("\\/r")
    IMM_REGEX = re.compile("i(.)")
    VALUE_REGEX = re.compile("c(.)")
    OPREG_REGEX = re.compile("r(.)")

class StandardInstruction(Instruction):
    def __init__(self, ins):
        super().__init__(ins)

        rex = InstructionCommon.REX_REGEX.search(self._opc)
        bytes = InstructionCommon.BYTES_REGEX.findall(self._opc)
        digit = InstructionCommon.DIGIT_REGEX.search(self._opc)
        modrm = InstructionCommon.MODRM_REGEX.search(self._opc)
        imm = InstructionCommon.IMM_REGEX.search(self._opc)
        value = InstructionCommon.VALUE_REGEX.search(self._opc)
        opreg = InstructionCommon.OPREG_REGEX.search(self._opc)
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

        print(self)
    
    def get_type(self):
        return InstructionType.STANDARD

    def has_modrm(self):
        return self.modrm or self.digit is not None
    
    def __str__(self):
        return f"{super().__str__()} digit {self.digit} modrm {self.modrm} imm {self.imm} value {self.value} opreg {self.opreg}"

class VEXInstruction(Instruction):
    def __init__(self, ins):
        raise NotImplementedError("VEX is not implemented")

class EVEXInstruction(Instruction):
    def __init__(self, ins):
        raise NotImplementedError("EVEX is not implemented")

def parse_instruction(ins):
    opc = ins.find("opc").text
    if "EVEX" in opc: return EVEXInstruction(ins)
    elif "VEX" in opc: return VEXInstruction(ins)
    else: return StandardInstruction(ins)

class InstructionGroup:
    def __init__(self, common):
        self.brief = common.find("brief").text
        self.instructions = [parse_instruction(ins) for ins in common.iter("ins")]

def parse_file(path):
    tree = ET.parse(path)
    root = tree.getroot()

    groups = [InstructionGroup(common) for common in root.iter("common")]
    return groups


if __name__ == "__main__":
    parse_file("xml/raw/x86/Intel/AZ.xml")