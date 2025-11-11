class BabyDuckError(Exception):
    """
    Clase que maneja todos los errores del compilador
    """
    def __init__(self, phase, subsection=None):
        # pagina: https://patorjk.com/software/taag/#p=testall&f=Graffiti&t=Cu%C3%A1druplos&x=none&v=4&h=4&w=80&we=false
        # Font de error por fase: Big Money-se
        # Font de error por subsección: Big

        self.semantic_error = """
         ______ _____  _____   ____  _____     ______ _   _ 
        |  ____|  __ \|  __ \ / __ \|  __ \   |  ____| \ | |
        | |__  | |__) | |__) | |  | | |__) |  | |__  |  \| |
        |  __| |  _  /|  _  /| |  | |  _  /   |  __| | . ` |
        | |____| | \ \| | \ \| |__| | | \ \   | |____| |\  |
        |______|_|  \_\_|  \_\\____/|_|  \_\  |______|_| \_|
                                                                                   
          _____ ______ __  __          _   _ _______ _____ _____ ____  
         / ____|  ____|  \/  |   /\   | \ | |__   __|_   _/ ____/ __ \ 
        | (___ | |__  | \  / |  /  \  |  \| |  | |    | || |   | |  | |
         \___ \|  __| | |\/| | / /\ \ | . ` |  | |    | || |   | |  | |
         ____) | |____| |  | |/ ____ \| |\  |  | |   _| || |___| |__| |
        |_____/|______|_|  |_/_/    \_\_| \_|  |_|  |_____\_____\____/                                                                                                          
        """

        self.vm_error = """
          ______ _____  _____   ____  _____     ______ _   _ 
         |  ____|  __ \|  __ \ / __ \|  __ \   |  ____| \ | |
         | |__  | |__) | |__) | |  | | |__) |  | |__  |  \| |
         |  __| |  _  /|  _  /| |  | |  _  /   |  __| | . ` |
         | |____| | \ \| | \ \| |__| | | \ \   | |____| |\  |
         |______|_|  \_\_|  \_\\____/|_|  \_\  |______|_| \_|
                                                                                                                                         
         __      ____  __ 
         \ \    / /  \/  |
          \ \  / /| \  / |
           \ \/ / | |\/| |
            \  /  | |  | |
             \/   |_|  |_|
        """
        
        self.phases = {
            "semantico": self.semantic_error,
            "vm": self.vm_error
        }

        full_message = self.format_message(phase, subsection)
        
        super().__init__(full_message)


    def format_message(self, phase, subsection):
        full_message = self.phase[phase] + "\n\n" + subsection + "\n\n============================================================================\n" + "============================================================================\n\n"
        return full_message