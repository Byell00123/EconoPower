from django.db import models

class Regiao(models.Model):
    nome = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        db_table = 'ins_regiao'
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'

class Estado(models.Model):
    nome = models.CharField(max_length=250)
    sigla = models.CharField(max_length=2)
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        db_table = 'ins_estado'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

class Cidade(models.Model):
    nome = models.CharField(max_length=250)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        db_table = 'ins_cidade'
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

class Instituicao_Tipo(models.Model):
    nome_simplificado = models.CharField(max_length=250, blank=True)
    nome_completo = models.CharField(max_length=250)
    sigla = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.nome_completo

    class Meta:
        db_table = 'ins_instituicao_tipo'
        verbose_name = 'Tipo da Instituição'
        verbose_name_plural = 'Tipos das Instituições'

class Endereco(models.Model):
    endereco_teste = models.CharField(max_length=250, blank=False)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    #TODO: Para fins de teste manter os 5 campos a baixo de fora dos teste
    # tipo_de_logradouro = models.CharField(max_length=250)
    # nome_de_logradouro = models.CharField(max_length=250)
    # numero = models.IntegerField(blank=True)
    # Complemento = models.CharField(max_length=250, blank=True) 
    # bairro = models.CharField(max_length=250)
    # cep = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.id

    class Meta:
        db_table = 'ins_endereco'
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

class Campus(models.Model):
    nome = models.CharField(max_length=250, blank=True)
    sigla = models.CharField(max_length=50, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    instituicao_tipo = models.ForeignKey(Instituicao_Tipo, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        db_table = 'ins_campus'
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'

class Bloco(models.Model):
    nome = models.CharField(max_length=255)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        db_table = 'ins_bloco'
        verbose_name = 'Bloco'
        verbose_name_plural = 'Blocos'

class Quadro_Energia(models.Model):
    bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.id

    class Meta:
        db_table = 'ins_quadro_energia'
        verbose_name = 'Quadro de Energia'
        verbose_name_plural = 'Quadros de Energia'

class Dado(models.Model):
    status = models.BooleanField(default=False)
    tensao = models.FloatField(default=0.00)
    corrente = models.FloatField(default=0.00)
    potencia = models.FloatField(default=0.00)

    def __str__(self) -> str:
        return self.id

    class Meta:
        db_table = 'ins_dado'
        verbose_name = 'Dado'
        verbose_name_plural = 'Dados'

class Localizacao(models.Model):
    latitude = models.FloatField(default=0.00)
    longitude = models.FloatField(default=0.00)

    def __str__(self) -> str:
        return self.id

    class Meta:
        db_table = 'ins_localizacao'
        verbose_name = 'Localização'
        verbose_name_plural = 'Localizações'

class Dispositivo(models.Model):
    quadro_energia = models.ForeignKey(Quadro_Energia, on_delete=models.CASCADE)
    dado = models.ForeignKey(Dado, on_delete=models.CASCADE)
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.id

    class Meta:
        db_table = 'ins_dispositivo'
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'

