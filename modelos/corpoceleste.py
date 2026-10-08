class CorpoCeleste:
    def __init__(self, id, nome, tipo, eh_planeta, massa,
                 gravidade, raio, dist_orbital, ao_redor_de, temp_media, num_luas):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.eh_planeta = eh_planeta
        self.massa = massa
        self.gravidade = gravidade
        self.raio = raio
        self.dist_orbital = dist_orbital
        self.ao_redor_de = ao_redor_de
        self.temp_media = temp_media
        self.num_luas = num_luas

    

    @staticmethod
    def from_api(d):
        massa = None
        m = d.get("mass")
        if m:                                    # vem como {massValue, massExponent}
            massa = m["massValue"] * 10 ** m["massExponent"]

        orbita = d.get("aroundPlanet")           # vem como {planet, rel} ou None
        return CorpoCeleste(
            id=d.get("id"),
            nome=d.get("englishName") or d.get("name"),
            tipo=d.get("bodyType"),
            eh_planeta=d.get("isPlanet", False),
            massa=massa,
            gravidade=d.get("gravity"),
            raio=d.get("meanRadius"),
            dist_orbital=d.get("semimajorAxis"),
            ao_redor_de=orbita["planet"] if orbita else None,
            temp_media=d.get("avgTemp"),
            num_luas=len(d.get("moons") or []),
        )

    def __str__(self):
        return f"{self.nome} ({self.tipo})"