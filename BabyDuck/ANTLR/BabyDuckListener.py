# Generated from BabyDuck.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .BabyDuckParser import BabyDuckParser
else:
    from BabyDuckParser import BabyDuckParser

# This class defines a complete listener for a parse tree produced by BabyDuckParser.
class BabyDuckListener(ParseTreeListener):

    # Enter a parse tree produced by BabyDuckParser#programa.
    def enterPrograma(self, ctx:BabyDuckParser.ProgramaContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#programa.
    def exitPrograma(self, ctx:BabyDuckParser.ProgramaContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#vars.
    def enterVars(self, ctx:BabyDuckParser.VarsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#vars.
    def exitVars(self, ctx:BabyDuckParser.VarsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#declarar_variables.
    def enterDeclarar_variables(self, ctx:BabyDuckParser.Declarar_variablesContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#declarar_variables.
    def exitDeclarar_variables(self, ctx:BabyDuckParser.Declarar_variablesContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#declarar_ids.
    def enterDeclarar_ids(self, ctx:BabyDuckParser.Declarar_idsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#declarar_ids.
    def exitDeclarar_ids(self, ctx:BabyDuckParser.Declarar_idsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#funcs.
    def enterFuncs(self, ctx:BabyDuckParser.FuncsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#funcs.
    def exitFuncs(self, ctx:BabyDuckParser.FuncsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#parametros.
    def enterParametros(self, ctx:BabyDuckParser.ParametrosContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#parametros.
    def exitParametros(self, ctx:BabyDuckParser.ParametrosContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#cuerpo.
    def enterCuerpo(self, ctx:BabyDuckParser.CuerpoContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#cuerpo.
    def exitCuerpo(self, ctx:BabyDuckParser.CuerpoContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#tipo.
    def enterTipo(self, ctx:BabyDuckParser.TipoContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#tipo.
    def exitTipo(self, ctx:BabyDuckParser.TipoContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#estatuto.
    def enterEstatuto(self, ctx:BabyDuckParser.EstatutoContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#estatuto.
    def exitEstatuto(self, ctx:BabyDuckParser.EstatutoContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#continuacion_de_estatuto_id.
    def enterContinuacion_de_estatuto_id(self, ctx:BabyDuckParser.Continuacion_de_estatuto_idContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#continuacion_de_estatuto_id.
    def exitContinuacion_de_estatuto_id(self, ctx:BabyDuckParser.Continuacion_de_estatuto_idContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#asigna.
    def enterAsigna(self, ctx:BabyDuckParser.AsignaContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#asigna.
    def exitAsigna(self, ctx:BabyDuckParser.AsignaContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#condicion.
    def enterCondicion(self, ctx:BabyDuckParser.CondicionContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#condicion.
    def exitCondicion(self, ctx:BabyDuckParser.CondicionContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#ciclo.
    def enterCiclo(self, ctx:BabyDuckParser.CicloContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#ciclo.
    def exitCiclo(self, ctx:BabyDuckParser.CicloContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#llamada.
    def enterLlamada(self, ctx:BabyDuckParser.LlamadaContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#llamada.
    def exitLlamada(self, ctx:BabyDuckParser.LlamadaContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#imprime.
    def enterImprime(self, ctx:BabyDuckParser.ImprimeContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#imprime.
    def exitImprime(self, ctx:BabyDuckParser.ImprimeContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#imprimir_elementos.
    def enterImprimir_elementos(self, ctx:BabyDuckParser.Imprimir_elementosContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#imprimir_elementos.
    def exitImprimir_elementos(self, ctx:BabyDuckParser.Imprimir_elementosContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#expresion.
    def enterExpresion(self, ctx:BabyDuckParser.ExpresionContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#expresion.
    def exitExpresion(self, ctx:BabyDuckParser.ExpresionContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#exp.
    def enterExp(self, ctx:BabyDuckParser.ExpContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#exp.
    def exitExp(self, ctx:BabyDuckParser.ExpContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#termino.
    def enterTermino(self, ctx:BabyDuckParser.TerminoContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#termino.
    def exitTermino(self, ctx:BabyDuckParser.TerminoContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#factor.
    def enterFactor(self, ctx:BabyDuckParser.FactorContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#factor.
    def exitFactor(self, ctx:BabyDuckParser.FactorContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#dato_o_llamada.
    def enterDato_o_llamada(self, ctx:BabyDuckParser.Dato_o_llamadaContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#dato_o_llamada.
    def exitDato_o_llamada(self, ctx:BabyDuckParser.Dato_o_llamadaContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#cte.
    def enterCte(self, ctx:BabyDuckParser.CteContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#cte.
    def exitCte(self, ctx:BabyDuckParser.CteContext):
        pass



del BabyDuckParser