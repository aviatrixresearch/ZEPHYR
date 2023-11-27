import osmium

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.buildings = []

    def node(self, n):
        if 'building' in n.tags:
            self.buildings.append(n)

handler = OSMHandler()
handler.apply_file("map.osm")

# Now, handler.buildings contains building data
