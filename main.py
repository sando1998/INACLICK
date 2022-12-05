from flask import Flask, make_response, jsonify, request
import re
import json

class Tradutor:
    def __init__(self, questao):
        self.questao = questao
  
    def tradutor(self, descricao):
        # Lista de conectivos utilizados
        conectivos = ["e", "ou", "então", "end", "and", "or", "^", "v", "~", "->"]
        outros_conectivos = ["se", "não"]

        # Tratando a questao
        descricao = descricao.lower().replace("  ", "")
        descricao = descricao + " end"
        questao = descricao.split()

        # Comecando a traducao
        questaoT = {}
        numS = 0
        qc = []
        qa = []
        for x in range(len(questao)):
            if questao[x] in conectivos:
                questaoT[str(numS)] = qa
                qa = []
                qc.append(numS)
                qc.append(questao[x])
                numS = numS + 1
            elif questao[x] in outros_conectivos:
                qc.append(questao[x])
            else:
                qa.append(questao[x])
        return {"questaoT": questaoT, "questaoComp": qc}

    def getObjective(self, description):
        if "negação" in description:
            return "not"
        elif "equivalente" or "equivalencia" in description:
            return "equiv"
        elif "consequencia" in description:
            return "conseq"
        else:
            return "unknown"

    def getAllInformationDescription(self):
        sent = re.split('"', self.questao)
        if len(sent) >= 3:
            return {"sentenca": sent[1], "objetivo": self.getObjective(sent[0] + " " + sent[2]), "traducao": self.tradutor(sent[1])}

app =  Flask('__name__')

@app.route('/Sentenças', methods = ['GET'])
def get_setencas():
    content = request.get_json()
    a = Tradutor(content['pergunta'])
    #print(a.getAllInformationDescription())
    #print(content['pergunta'])
    #funcaoRafa(a.getAllInformationDescription())
    #retornar oque vem do rafa pro Antero
    return json.dumps(a.getAllInformationDescription())


app.run()

#{
#	"pergunta" : "Considere a sentença: \"Paulo é torcedor do Nacional ou Débora não é torcedora do Fast\" A negação lógica dessa sentença é"
#} IMSOMNIA
