import zlib
import urllib.parse
import base64

raw_xml = '<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="2" value="Hello" vertex="1" parent="1"><mxGeometry x="20" y="20" width="80" height="30" as="geometry"/></mxCell></root></mxGraphModel>'

# Test roundtrip
encoded = urllib.parse.quote(raw_xml, safe='~()*!.\'')
compressor = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15, memLevel=8, strategy=0)
deflated = compressor.compress(encoded.encode('utf-8')) + compressor.flush()
b64 = base64.b64encode(deflated).decode('utf-8')

# Decompress
decoded_b64 = base64.b64decode(b64)
decompressor = zlib.decompressobj(wbits=-15)
inflated = decompressor.decompress(decoded_b64) + decompressor.flush()
restored_xml = urllib.parse.unquote(inflated.decode('utf-8'))

print('Roundtrip match:', raw_xml == restored_xml)
print('Compressed length:', len(b64))
