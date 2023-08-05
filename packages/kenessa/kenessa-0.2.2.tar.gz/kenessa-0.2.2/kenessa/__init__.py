import sqlite3
import re
from pkg_resources import resource_filename
conn = sqlite3.connect(resource_filename(__name__, 'kenessa.db'))


class Kenessa:
    def __init__(self):
        self.c = conn.cursor()

    def get_province(self):
        """Returns a list of all provinces in Rwanda"""
        self.c.execute('SELECT * FROM Province')
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_district(self, province):
        """Returns a list (json format) of all district belonging to the province passed in parameter"""
        query = "SELECT District.id,District.name \
                FROM District INNER JOIN Province ON District.province_id = Province.id \
                WHERE Province.id IN ({seq})".format(seq=','.join(['?'] * len(province)))
        self.c.execute(query, province)
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_sector(self, district):
        """Returns a list (json format) of all sectors belonging to the district passed in parameter"""
        query = "SELECT Sector.id,Sector.name \
                FROM Sector INNER JOIN District ON Sector.district_id = District.id \
                WHERE District.id IN ({seq})".format(seq=','.join(['?'] * len(district)))
        self.c.execute(query, district)
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_cell(self, sector):
        """Returns a list (json format) of all cells belonging to the sector passed in parameter"""
        query = "SELECT Cell.id,Cell.name\
                FROM Cell INNER JOIN Sector ON Cell.sector_id= Sector.id \
                WHERE Sector.id IN ({seq})".format(seq=','.join(['?'] * len(sector)))
        self.c.execute(query, sector)
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_village(self, cell):
        """Returns a list (json format) of all villages belonging to the cell passed in parameter"""
        query = "SELECT Village.id,Village.name \
                FROM Village INNER JOIN Cell ON Village.cell_id = Cell.id \
                WHERE Cell.id IN ({seq})".format(seq=','.join(['?'] * len(cell)))
        self.c.execute(query, cell)
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_all_from_village_id(self, village):
        """Returns in json format a list of cell, sector, district and Province
        in which belongs the village passed in parameter """
        output = dict()
        self.c.execute("SELECT Village.id FROM Village WHERE Village.id = ?", [village])
        id_village = self.c.fetchall()

        if village is None:
            k = ['cell', 'district', 'sector', 'province']
            output = dict.fromkeys(k)
            return output

        # Village
        village = dict()
        village['id'] = str(list(id_village[0])[0])
        village['name'] = self.get_name_from_id(str(list(id_village[0])[0]))
        output['village'] = village
        # id cell
        m_cell = re.search("\d{6}", str(list(id_village[0])[0]))
        cell_info = {'id': m_cell.group()}
        cell_info['name'] = self.get_name_from_id(m_cell.group())
        output['cell'] = cell_info
        # id sector
        m_sector = re.search("\d{4}", str(list(id_village[0])[0]))
        sector_info = {"id": m_sector.group()}
        sector_info['name'] = self.get_name_from_id(m_sector.group())
        output['sector'] = sector_info
        # id district
        m_district = re.search("\d{2}", str(list(id_village[0])[0]))
        district_info = {"id": m_district.group()}
        district_info['name'] = self.get_name_from_id(m_district.group())
        output['district'] = district_info
        # id province
        m_province = re.search("\d{1}", str(list(id_village[0])[0]))
        province_info = {"id": m_province.group()}
        province_info['name'] = self.get_name_from_id(m_province.group())
        output['province'] = province_info

        return(output)

    def get_name_from_id(self, idt):
        """Returns the name (string) of the corresponding id """
        if len(idt) == 1:
            self.c.execute("SELECT Province.name FROM Province WHERE Province.id = ?", [idt])
            # return(self.c.fetchall())
            p_name = self.c.fetchall()
            return str(list(p_name[0])[0])
        if len(idt) == 2:
            self.c.execute("SELECT District.name FROM District WHERE District.id = ?", [idt])
            # return(self.c.fetchall())
            d_name = self.c.fetchall()
            return str(list(d_name[0])[0])
        if len(idt) == 4:
            self.c.execute("SELECT Sector.name FROM Sector WHERE Sector.id = ?", [idt])
            # return(self.c.fetchall())
            s_name = self.c.fetchall()
            return str(list(s_name[0])[0])
        if len(idt) == 6:
            self.c.execute("SELECT Cell.name FROM Cell WHERE Cell.id = ?", [idt])
            # return(self.c.fetchall())
            c_name = self.c.fetchall()
            return str(list(c_name[0])[0])
        if len(idt) == 8:
            self.c.execute("SELECT Village.name FROM Village WHERE Village.id = ?", [idt])
            # return(self.c.fetchall())
            v_name = self.c.fetchall()
            return str(list(v_name[0])[0])

    def ken_filter(self, villages):
        province = list()
        district = list()
        sector = list()
        cell = list()

        data = list()
        villages = sorted(set(villages))
        for village in villages:
            location = self.get_all_from_village_id(village)
            province.append(location['province']['id'])
            district.append(location['district']['id'])
            sector.append(location['sector']['id'])
            cell.append(location['cell']['id'])

        province = sorted(set(province))
        district = sorted(set(district))
        sector = sorted(set(sector))
        cell = sorted(set(cell))

        for p in province:
            json_p = dict()
            json_p['name'] = self.get_name_from_id(p)
            json_p['id'] = p
            list_d = list()
            get_districts = self.get_district(p)
            for d in district:
                json_d = dict()

                for get_d in get_districts:
                    if str(d) == str(get_d['id']):
                        json_d['name'] = self.get_name_from_id(d)
                        json_d['id'] = d
                        list_s = list()
                        get_sectors = self.get_sector([d])
                        for s in sector:
                            json_s = dict()
                            for get_s in get_sectors:
                                if str(s) == str(get_s['id']):
                                    json_s['name'] = self.get_name_from_id(s)
                                    json_s['id'] = s
                                    list_c = list()
                                    get_cells = self.get_cell([s])
                                    for c in cell:
                                        json_c = dict()
                                        for get_c in get_cells:
                                            if str(c) == str(get_c['id']):
                                                json_c['name'] = self.get_name_from_id(c)
                                                json_c['id'] = c
                                                get_villages = self.get_village([c])
                                                list_v = list()
                                                for v in villages:
                                                    json_v = dict()
                                                    for get_v in get_villages:
                                                        if str(v) == str(get_v['id']):
                                                            json_v['name'] = self.get_name_from_id(v)
                                                            json_v['id'] = v
                                                            list_v.append(json_v)
                                                json_c['village'] = list_v
                                                list_c.append(json_c)
                                    json_s['cell'] = list_c
                                    list_s.append(json_s)
                        json_d['sector'] = list_s
                        list_d.append(json_d)
            json_p['district'] = list_d
            data.append(json_p)

        return data