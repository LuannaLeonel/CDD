from functools import reduce

import bs4 as bs4


class DataScrapy:
    def __init__(self, response):
        self.response = response

    def run(self, gender):
        nome, birthday = self.general_info()
        gastos_parlamentar = self.gastos_par()
        gastos_gabinete = self.gastos_gab()
        salario_bruto = self.salario_bruto()
        presenca = self.presenca()

        return {
            "genero": gender,
            "nome": nome,
            "data_nascimento": birthday,
            **gastos_parlamentar,
            **gastos_gabinete,
            **presenca,
            "salario_bruto": salario_bruto
        }

    def presenca(self):
        def parse_presenca_to_int(presenca):
            return int(presenca.strip().split(" ")[0].strip())

        soup = bs4.BeautifulSoup(self.response.body, "html")
        presencas = soup.find_all("dd", {"class": "list-table__definition-description"})

        if presencas:
            return {
                "presenca_plenario": parse_presenca_to_int(presencas[0].get_text()),
                "ausencia_plenario": parse_presenca_to_int(presencas[1].get_text()) + parse_presenca_to_int(
                    presencas[2].get_text()),
                "ausencia_justificada_plenario": parse_presenca_to_int(presencas[2].get_text()),
                "presenca_comissao": parse_presenca_to_int(presencas[3].get_text()),
                "ausencia_comissao": parse_presenca_to_int(presencas[4].get_text()) + parse_presenca_to_int(
                    presencas[5].get_text()),
                "ausencia_justificada_comissao": parse_presenca_to_int(presencas[5].get_text())
            }

        return {
            "presenca_plenario": 0,
            "ausencia_plenario": 0,
            "ausencia_justificada_plenario": 0,
            "presenca_comissao": 0,
            "ausencia_comissao": 0,
            "ausencia_justificada_comissao": 0
        }

    def general_info(self):
        name_xpath_id, birth_date_xpath_id = [1, 5]

        name_path = f'//*[@id="identificacao"]/div/div/div[3]/div/div/div[2]/div[1]/ul/li[{name_xpath_id}]/text()'
        name = self.response.xpath(name_path).get().strip()

        birth_path = f'//*[@id="identificacao"]/div/div/div[3]/div/div/div[2]/div[1]/ul/li[{birth_date_xpath_id}]/text()'
        birth_date = self.response.xpath(birth_path).get().strip()

        return name, birth_date

    def gastos_par(self):
        soup = bs4.BeautifulSoup(self.response.body, "html")
        gastos_parlamentar = soup.find_all("table", {"id": "gastomensalcotaparlamentar"})[0].find_all("td")

        gastos_serializados = self.parse_gastos(gastos_parlamentar)
        soma_gastos = self.soma_gastos(gastos_serializados)
        return {
            "gasto_total_par": soma_gastos,
            "gasto_jan_par": gastos_serializados[0]["gasto"] if gastos_serializados[0:] else 0.0,
            "gasto_fev_par": gastos_serializados[1]["gasto"] if gastos_serializados[1:] else 0.0,
            "gasto_mar_par": gastos_serializados[2]["gasto"] if gastos_serializados[2:] else 0.0,
            "gasto_abr_par": gastos_serializados[3]["gasto"] if gastos_serializados[3:] else 0.0,
            "gasto_maio_par": gastos_serializados[4]["gasto"] if gastos_serializados[4:] else 0.0,
            "gasto_junho_par": gastos_serializados[5]["gasto"] if gastos_serializados[5:] else 0.0,
            "gasto_jul_par": gastos_serializados[6]["gasto"] if gastos_serializados[6:] else 0.0,
            "gasto_agosto_par": gastos_serializados[7]["gasto"] if gastos_serializados[7:] else 0.0,
            "gasto_set_par": gastos_serializados[8]["gasto"] if gastos_serializados[8:] else 0.0,
            "gasto_out_par": gastos_serializados[9]["gasto"] if gastos_serializados[9:] else 0.0,
            "gasto_nov_par": gastos_serializados[10]["gasto"] if gastos_serializados[10:] else 0.0,
            "gasto_dez_par": gastos_serializados[11]["gasto"] if gastos_serializados[11:] else 0.0,
        }

    def gastos_gab(self):
        soup = bs4.BeautifulSoup(self.response.body, "html")
        gastos_gabinete = soup.find_all("table", {"id": "gastomensalverbagabinete"})[0].find_all("td")

        gastos_serializados = self.parse_gastos(gastos_gabinete)
        soma_gastos = self.soma_gastos(gastos_serializados)
        return {

            "gasto_total_gab": soma_gastos,
            "gasto_jan_gab": gastos_serializados[0]["gasto"] if gastos_serializados[0:] else 0.0,
            "gasto_fev_gab": gastos_serializados[1]["gasto"] if gastos_serializados[1:] else 0.0,
            "gasto_mar_gab": gastos_serializados[2]["gasto"] if gastos_serializados[2:] else 0.0,
            "gasto_abr_gab": gastos_serializados[3]["gasto"] if gastos_serializados[3:] else 0.0,
            "gasto_maio_gab": gastos_serializados[4]["gasto"] if gastos_serializados[4:] else 0.0,
            "gasto_junho_gab": gastos_serializados[5]["gasto"] if gastos_serializados[5:] else 0.0,
            "gasto_jul_gab": gastos_serializados[6]["gasto"] if gastos_serializados[6:] else 0.0,
            "gasto_agosto_gab": gastos_serializados[7]["gasto"] if gastos_serializados[7:] else 0.0,
            "gasto_set_gab": gastos_serializados[8]["gasto"] if gastos_serializados[8:] else 0.0,
            "gasto_out_gab": gastos_serializados[9]["gasto"] if gastos_serializados[9:] else 0.0,
            "gasto_nov_gab": gastos_serializados[10]["gasto"] if gastos_serializados[10:] else 0.0,
            "gasto_dez_gab": gastos_serializados[11]["gasto"] if gastos_serializados[11:] else 0.0,
        }

    def salario_bruto(self):
        salary_text = self.response.xpath(
            '//*[@id="recursos-section"]/ul/li[2]/div/a/text()'
        ).get()

        salary = float(salary_text.split("\n")[1].replace(".", "").replace(",", "."))

        return salary

    def parse_gastos(self, tabela):
        gastos = []

        for td in range(0, len(tabela), 3):
            gastos.append({
                "mes": tabela[td].get_text(),
                "gasto": self.convert(tabela[td + 1].get_text())
            })

        return gastos

    def soma_gastos(self, gastos):
        gastos_valor = [gasto["gasto"] for gasto in gastos]
        return reduce(lambda a, b: a + b, gastos_valor)

    def convert(self, brl_num):
        return float(brl_num.replace(".", '').replace(",", ".").strip())
