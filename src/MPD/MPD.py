# https://github.com/redlean91/MPD-Serializer
# MPD Serializer for Just Dance
# Serializer for Media Presentation Description files to Just Dance-like format

from MPD.CSerializerObject import CSerializerObject
from MPD.XML import XML
from io import BytesIO
import re

class MPD:
    def __init__(self, mpd_path, fileStream, add_jd_url=True):
        self.mpd_json = XML(xml_file=mpd_path).Cook()
        self.fileStream = fileStream
        self.add_jd_url = add_jd_url
    
    def Serialize(self):
        @staticmethod
        def __dash_attributes(attributes):
            @staticmethod
            def __type(type="static"):
                # I saw that the most used type of the game
                # was static, and i dont know if it uses
                # any other type. So thats what ill keep for now.
                return {"static": 0}[type]

            fileStream = BytesIO()
            
            fileStream.write(CSerializerObject.uint8(__type(attributes["type"])))
            fileStream.write(CSerializerObject.float32(float(attributes["mediaPresentationDuration"].replace("PT", "").replace("S", ""))))
            fileStream.write(CSerializerObject.float32(float(attributes["minBufferTime"].replace("PT", "").replace("S", ""))))

            return fileStream.getvalue()

        @staticmethod
        def __add_jd_url(url):
            MapName =  re.sub(r'_(LOW|MID|HIGH|ULTRA|LOW.hd|MID.hd|HIGH.hd|ULTRA.hd)\.webm$', '.webm', url, flags=re.IGNORECASE).replace(".webm", "")
            return f"jmcs://jd-contents/{MapName}/{url}"
        
        mpd = self.mpd_json["{urn:mpeg:DASH:schema:MPD:2011}MPD"]

        self.fileStream.write(CSerializerObject.uint32(1)) # Endianness check
        self.fileStream.write(__dash_attributes(attributes=mpd["@attributes"]))
        
        period_entries = len(mpd) - 1 # Subtracting 1 for @attributes
        self.fileStream.write(CSerializerObject.uint32(period_entries))
        
        for i in range(period_entries):
            key = list(mpd.keys())[i+1]
            period_data = mpd[key]

            self.fileStream.write(CSerializerObject.uint32(int(period_data["@attributes"]["id"])))
            self.fileStream.write(CSerializerObject.float32(float(period_data["@attributes"]["start"].replace("PT", "").replace("S", ""))))
            self.fileStream.write(CSerializerObject.float32(float(period_data["@attributes"]["duration"].replace("PT", "").replace("S", ""))))

            adaptationSet_entries = len(period_data) - 1 # Subtracting 1 for @attributes
            self.fileStream.write(CSerializerObject.uint32(adaptationSet_entries))

            for j in range(adaptationSet_entries):
                key = list(period_data.keys())[j+1]
                adaptationSet_data = period_data[key]

                self.fileStream.write(CSerializerObject.uint32(int(adaptationSet_data["@attributes"]["id"])))
                self.fileStream.write(CSerializerObject.String8(adaptationSet_data["@attributes"]["mimeType"]))
                self.fileStream.write(CSerializerObject.String8(adaptationSet_data["@attributes"]["codecs"]))
                self.fileStream.write(CSerializerObject.uint32(int(adaptationSet_data["@attributes"].get("maxWidth", 1216))))
                self.fileStream.write(CSerializerObject.uint32(int(adaptationSet_data["@attributes"].get("maxHeight", 720))))
                self.fileStream.write(CSerializerObject.uint32(0x0)) # dont really know whats this tbh
                self.fileStream.write(CSerializerObject.uint32(1 if adaptationSet_data["@attributes"]["subsegmentAlignment"] == "true" else 0))
                self.fileStream.write(CSerializerObject.uint8(int(adaptationSet_data["@attributes"]["subsegmentStartsWithSAP"])))
                self.fileStream.write(CSerializerObject.uint8(1 if adaptationSet_data["@attributes"]["bitstreamSwitching"] == "true" else 0))

                representation_entries = len(adaptationSet_data) - 1 # Subtracting 1 for @attributes

                for k in range(representation_entries):
                    key = list(adaptationSet_data.keys())[k+1]
                    representation_data_entries = adaptationSet_data[key]

                    representations_data_entries = len(representation_data_entries)
                    self.fileStream.write(CSerializerObject.uint32(representations_data_entries))
                    
                    for representation in representation_data_entries:
                        self.fileStream.write(CSerializerObject.uint32(int(representation["@attributes"]["id"])))
                        self.fileStream.write(CSerializerObject.uint32(int(representation["@attributes"]["bandwidth"])))
                        self.fileStream.write(CSerializerObject.String8(representation["{urn:mpeg:DASH:schema:MPD:2011}BaseURL"] if not self.add_jd_url else __add_jd_url(representation["{urn:mpeg:DASH:schema:MPD:2011}BaseURL"])))

                        segment_base = representation["{urn:mpeg:DASH:schema:MPD:2011}SegmentBase"]

                        indexRange = segment_base["@attributes"]["indexRange"].split("-")
                        _range = segment_base["{urn:mpeg:DASH:schema:MPD:2011}Initialization"]["@attributes"]["range"].split("-")

                        self.fileStream.write(CSerializerObject.uint32(int(_range[0])))
                        self.fileStream.write(CSerializerObject.uint32(int(_range[1])))
                        self.fileStream.write(CSerializerObject.uint32(int(indexRange[0])))
                        self.fileStream.write(CSerializerObject.uint32(int(indexRange[1])))