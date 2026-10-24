import json, sys, os, hashlib, datetime
import pefile

sys.stdout.reconfigure(encoding="utf-8")

TARGET = r"<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111.exe"
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"
os.makedirs(OUT, exist_ok=True)

pe = pefile.PE(TARGET, fast_load=False)

lines = []
def w(s=""):
    lines.append(s)
    print(s)

w("=" * 70)
w("PE 元信息")
w("=" * 70)
fh = pe.FILE_HEADER
w(f"Machine            : 0x{fh.Machine:04X}  ({'i386' if fh.Machine==0x14c else 'other'})")
w(f"NumberOfSections   : {fh.NumberOfSections}")
w(f"TimeDateStamp      : 0x{fh.TimeDateStamp:08X}  ({datetime.datetime.utcfromtimestamp(fh.TimeDateStamp)} UTC)")
w(f"Characteristics    : 0x{fh.Characteristics:04X}")
w(f"SizeOfOptionalHdr  : {fh.SizeOfOptionalHeader}")
oh = pe.OPTIONAL_HEADER
w(f"Magic              : 0x{oh.Magic:04X}  ({'PE32' if oh.Magic==0x10b else 'PE32+'})")
w(f"Subsystem          : {oh.Subsystem}  ({pefile.SUBSYSTEM_TYPE.get(oh.Subsystem, '?')})")
w(f"LinkerVersion      : {oh.MajorLinkerVersion}.{oh.MinorLinkerVersion}")
w(f"OSVersion          : {oh.MajorOperatingSystemVersion}.{oh.MinorOperatingSystemVersion}")
w(f"SubsysVersion      : {oh.MajorSubsystemVersion}.{oh.MinorSubsystemVersion}")
w(f"ImageBase          : 0x{oh.ImageBase:08X}")
w(f"EntryPoint (RVA)   : 0x{oh.AddressOfEntryPoint:08X}")
w(f"SizeOfImage        : 0x{oh.SizeOfImage:X}")
w(f"DllCharacteristics : 0x{oh.DllCharacteristics:04X}")
w(f"CheckSum           : 0x{oh.CheckSum:08X}")

w()
w("=" * 70)
w("节区")
w("=" * 70)
w(f"{'Name':<10}{'VA':>10}{'VSize':>10}{'RawPtr':>10}{'RawSize':>10}{'Entropy':>9}{'Flags':>12}")
for s in pe.sections:
    name = s.Name.rstrip(b"\x00").decode("latin1")
    w(f"{name:<10}{s.VirtualAddress:>10X}{s.Misc_VirtualSize:>10X}"
      f"{s.PointerToRawData:>10X}{s.SizeOfRawData:>10X}"
      f"{s.get_entropy():>9.3f}{s.Characteristics:>12X}")

w()
w("=" * 70)
w("导入表")
w("=" * 70)
if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
    for e in pe.DIRECTORY_ENTRY_IMPORT:
        w(f"\n[{e.dll.decode('latin1')}]")
        for imp in e.imports:
            nm = imp.name.decode("latin1") if imp.name else f"ord#{imp.ordinal}"
            w(f"    {nm}")
else:
    w("(无导入表)")

w()
w("=" * 70)
w("导出表 / 延迟导入 / TLS")
w("=" * 70)
w(f"Export dir        : {'有' if hasattr(pe,'DIRECTORY_ENTRY_EXPORT') else '无'}")
w(f"Delay import dir  : {'有' if hasattr(pe,'DIRECTORY_ENTRY_DELAY_IMPORT') else '无'}")
w(f"TLS dir           : {'有' if hasattr(pe,'DIRECTORY_ENTRY_TLS') else '无'}")
w(f"Rich header       : {'有' if hasattr(pe,'RICH_HEADER') and pe.RICH_HEADER else '无'}")

w()
w("=" * 70)
w("资源树")
w("=" * 70)
RES_TYPES = {1:"CURSOR",2:"BITMAP",3:"ICON",4:"MENU",5:"DIALOG",6:"STRING",
             9:"ACCELERATOR",10:"RCDATA",11:"MESSAGETABLE",12:"GROUP_CURSOR",
             14:"GROUP_ICON",16:"VERSION",24:"MANIFEST"}
def walk(entries, depth=1):
    for e in entries:
        if hasattr(e, "directory"):
            walk(e.directory.entries, depth + 1)
        else:
            d = e.data.struct
            name = e.name
            if isinstance(name, int):
                label = RES_TYPES.get(name, f"type{name}") if depth == 1 else str(name)
            else:
                label = str(name)
            w(f"{'  '*(depth-1)}{label:<20} off=0x{d.OffsetToData:08X} size={d.Size}")

walk(pe.DIRECTORY_ENTRY_RESOURCE.entries if hasattr(pe, "DIRECTORY_ENTRY_RESOURCE") else [])

w()
w("=" * 70)
w("节区完整性/签名")
w("=" * 70)
sec = pe.OPTIONAL_HEADER.DATA_DIRECTORY[4]
w(f"Security dir VA=0x{sec.VirtualAddress:X} Size={sec.Size}")

with open(os.path.join(OUT, "pe_info.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n[saved] pe_info.txt")
