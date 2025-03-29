class Helloworld: 
    name: str
    date: int
    
    def __init__(self, **kwargs):
        print('kwargs')
        for key, value in kwargs.items():
              setattr(self, key, value)
              
    # def __init__(self, *, name:str, date): On peut typer directement le param
    # hello = HelloWorld(name="toto", date="2022") 
    # hello = HelloWorld(date="2022", name="toto")  

    # def __init__(self, name, date):
    # hello = HelloWorld(name="toto", date="2022") 
    # hello = HelloWorld(date="2022", name="toto") 
    # hello = HelloWorld("toto", "2022")
    
    # def __init__(self, /, name, date):
    # hello = HelloWorld("toto", "2022")
    
    """
    Si ce n'est pas static on ajoute self auquel cas on met @staticmethod
    """
    def greet(self)->str: #Typage du retour de la fonction
        return f"Hello world {self.name}"