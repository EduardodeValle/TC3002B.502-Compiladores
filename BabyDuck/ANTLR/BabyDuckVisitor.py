# Generated from BabyDuck.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .BabyDuckParser import BabyDuckParser
else:
    from BabyDuckParser import BabyDuckParser

# This class defines a complete generic visitor for a parse tree produced by BabyDuckParser.

class BabyDuckVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BabyDuckParser#programa.
    def visitPrograma(self, ctx:BabyDuckParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#vars.
    def visitVars(self, ctx:BabyDuckParser.VarsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#declarar_variables.
    def visitDeclarar_variables(self, ctx:BabyDuckParser.Declarar_variablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#declarar_ids.
    def visitDeclarar_ids(self, ctx:BabyDuckParser.Declarar_idsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#funcs.
    def visitFuncs(self, ctx:BabyDuckParser.FuncsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#parametros.
    def visitParametros(self, ctx:BabyDuckParser.ParametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#cuerpo.
    def visitCuerpo(self, ctx:BabyDuckParser.CuerpoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#tipo.
    def visitTipo(self, ctx:BabyDuckParser.TipoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#devuelve.
    def visitDevuelve(self, ctx:BabyDuckParser.DevuelveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#estatuto.
    def visitEstatuto(self, ctx:BabyDuckParser.EstatutoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#continuacion_de_estatuto_id.
    def visitContinuacion_de_estatuto_id(self, ctx:BabyDuckParser.Continuacion_de_estatuto_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#condicion.
    def visitCondicion(self, ctx:BabyDuckParser.CondicionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#ciclo.
    def visitCiclo(self, ctx:BabyDuckParser.CicloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#imprime.
    def visitImprime(self, ctx:BabyDuckParser.ImprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#imprimir_elementos.
    def visitImprimir_elementos(self, ctx:BabyDuckParser.Imprimir_elementosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#expresion.
    def visitExpresion(self, ctx:BabyDuckParser.ExpresionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#exp.
    def visitExp(self, ctx:BabyDuckParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#termino.
    def visitTermino(self, ctx:BabyDuckParser.TerminoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#factor.
    def visitFactor(self, ctx:BabyDuckParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#dato_o_llamada.
    def visitDato_o_llamada(self, ctx:BabyDuckParser.Dato_o_llamadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BabyDuckParser#cte.
    def visitCte(self, ctx:BabyDuckParser.CteContext):
        return self.visitChildren(ctx)



del BabyDuckParser