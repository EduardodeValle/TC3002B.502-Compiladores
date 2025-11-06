class BabyDuckError(Exception):
    """
    Clase que maneja todos los errores del compilador
    """
    def __init__(self, phase, subsection):
        # pagina: https://patorjk.com/software/taag/#p=testall&f=Graffiti&t=Cu%C3%A1druplos&x=none&v=4&h=4&w=80&we=false
        # Font de error por fase: Big Money-se
        # Font de error por subsección: Big

        self.semantic_error = """
           _____                            _   _           
          / ____|                          | | (_)          
         | (___   ___ _ __ ___   __ _ _ __ | |_ _  ___ ___  
          \___ \ / _ \ '_ ` _ \ / _` | '_ \| __| |/ __/ _ \ 
          ____) |  __/ | | | | | (_| | | | | |_| | (_| (_) |
         |_____/ \___|_| |_| |_|\__,_|_| |_|\__|_|\___\___/                                                                                                          
        """

        self.quadruples_error = """
           _____                _                  _           
          / ____|              | |                | |          
         | |    _   _  __ _  __| |_ __ _   _ _ __ | | ___  ___ 
         | |   | | | |/ _` |/ _` | '__| | | | '_ \| |/ _ \/ __|
         | |___| |_| | (_| | (_| | |  | |_| | |_) | | (_) \__ \
          \_____\__,_|\__,_|\__,_|_|   \__,_| .__/|_|\___/|___/
                                            | |                
                                            |_|                                          
        """

        self.vm_error = """
         __      ____  __ 
         \ \    / /  \/  |
          \ \  / /| \  / |
           \ \/ / | |\/| |
            \  /  | |  | |
             \/   |_|  |_|
        """
        
        self.phases = {
            "semantico": self.semantic_error,
            "cuadruplos": self.quadruples_error,
            "vm": self.vm_error
        }

        full_message = self.format_message(phase, subsection)
        
        super().__init__(full_message)


    def format_message(self, phase, subsection):
        full_message = self.phase[phase] + "\n\n" + subsection + "\n\n============================================================================\n" + "============================================================================\n\n"
        return full_message