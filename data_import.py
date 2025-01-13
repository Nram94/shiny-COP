import pandas as pd
from pathlib import Path
from shiny import ui

app_dir = Path(__file__).parent
### Obtener filepaths para los .csv

file_path_evaluadores = app_dir/"evaluadores.csv"
flie_path_competencias = app_dir/"competencias.xlsx"
flie_path_competencia_evaluador_rol = app_dir/"competencia_evaluador_rol.xlsx"

### Crear dataframes
evaluadores = pd.read_csv(file_path_evaluadores)
competencias = pd.read_excel(flie_path_competencias)
competencia_evaluador_rol = pd.read_excel(flie_path_competencia_evaluador_rol)
names_list = [
    "",
    "Luisa Fernanda Correa",
    "Cristina Duque R.",
    "Jancelly Pérez L",
    "Paula Alzate D.",
    "Deisy Morales C.",
    "Mónica Dávila B.",
    "Oscar Berrío C.",
    "Jonathan Rios G",
    "Catalina Lopera R.",
    "Miguel Angel Aguirre",
    "Mariana Ruiz",
    "Luis Fernando Marin",
    "Lina Marcela Henao",
    "Yaneth Milena Garcia",
    "Carolina Granados G",
    "Manuela Pino T.",
    "Patricia Pérez C.",
    "Leifer David Zapata",
    "Valentina Vélez",
    "Nicole Rios Perez",
    "Juliana Morales Parada",
    "Laura Cordoba",
    "Valentina Muriel"
]

### Esquema de inputs de UI.
INPUTS = {
    "name_evaluador": ui.input_select(
        "name_evaluador",
        "Seleccione su nombre:",
        choices = names_list,
        selected=[]
        ),
    "rol_evaluador":ui.input_select(
        "rol_evaluador",
        "Rol del evaluador",
        choices = ["", "Líder", "Partner", "Cliente Interno", "Autoevaluación"]
        ),
    "name_evaluado": ui.input_select(
        "name_evaluado",
        "Seleccione nombre de la persona a evaluar:",
        choices = names_list,
        selected=[]
        ),
    "cargo_evaluado": ui.input_select(
        "cargo_evaluado",
        "Cargo del evaluado",
        choices=["", "Analista", "Auxiliar", "Director", "Médico"],
    ),
    "cargo_evaluado_auto": ui.input_select(
        "cargo_evaluado_auto",
        "Cargo",
        choices=["", "Analista", "Auxiliar", "Director", "Médico"],
    ),
    # Decisión y Liderazgo
    # cluster1:
    "cl1_comp1_descriptors": ui.input_radio_buttons(
        id="cl1_comp1_descriptors",
        label="Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[0]}', 
                 f'2 - {competencias.descriptor2[0]}', 
                 f'3 - {competencias.descriptor3[0]}'],
        selected=[],
        inline=True,
    ),
    "cl1_comp2_descriptors": ui.input_radio_buttons(
        id="cl1_comp2_descriptors",
        label="Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[1]}', 
                 f'2 - {competencias.descriptor2[1]}', 
                 f'3 - {competencias.descriptor3[1]}'],
        selected=[],
        inline=True,
    ),

    "cl1_comp3_descriptors": ui.input_radio_buttons(
        "cl1_comp3_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[2]}', 
                 f'2 - {competencias.descriptor2[2]}', 
                 f'3 - {competencias.descriptor3[2]}'],
        selected=[],
        inline=True,
    ),

    "cl1_comp4_descriptors": ui.input_radio_buttons(
        "cl1_comp4_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[3]}', 
                 f'2 - {competencias.descriptor2[3]}', 
                 f'3 - {competencias.descriptor3[3]}'],
        selected=[],
        inline=True,
    ),
    
    # Equipo e Integridad
    # "cluster2":{
    "cl2_comp1_descriptors": ui.input_radio_buttons(
        "cl2_comp1_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[4]}', 
                 f'2 - {competencias.descriptor2[4]}', 
                 f'3 - {competencias.descriptor3[4]}'],
        selected=[],
        inline=True,
    ),
    "cl2_comp2_descriptors": ui.input_radio_buttons(
        "cl2_comp2_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[5]}', 
                 f'2 - {competencias.descriptor2[5]}', 
                 f'3 - {competencias.descriptor3[5]}'],
        selected=[],
        inline=True,
    ),
    # },
    # Relaciones e Influencia
    # "cluster3":{
    "cl3_comp1_descriptors": ui.input_radio_buttons(
        "cl3_comp1_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[6]}', 
                 f'2 - {competencias.descriptor2[6]}', 
                 f'3 - {competencias.descriptor3[6]}'],
        selected=[],
        inline=True,
    ),
    "cl3_comp2_descriptors": ui.input_radio_buttons(
        "cl3_comp2_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[7]}', 
                 f'2 - {competencias.descriptor2[7]}', 
                 f'3 - {competencias.descriptor3[7]}'],
        selected=[],
        inline=True,
    ),
    "cl3_comp3_descriptors": ui.input_radio_buttons(
        "cl3_comp3_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[8]}', 
                 f'2 - {competencias.descriptor2[8]}', 
                 f'3 - {competencias.descriptor3[8]}'],
        selected=[],
        inline=True,
    ),
    # },
    # Análisis y Reportes
    # "cluster4":{
    "cl4_comp1_descriptors": ui.input_radio_buttons(
        "cl4_comp1_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[9]}', 
                 f'2 - {competencias.descriptor2[9]}', 
                 f'3 - {competencias.descriptor3[9]}'],
        selected=[],
        inline=True,
    ),
    "cl4_comp2_descriptors": ui.input_radio_buttons(
        "cl4_comp2_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[10]}', 
                 f'2 - {competencias.descriptor2[10]}', 
                 f'3 - {competencias.descriptor3[10]}'],
        selected=[],
        inline=True,
    ),
    "cl4_comp3_descriptors": ui.input_radio_buttons(
        "cl4_comp3_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[11]}', 
                 f'2 - {competencias.descriptor2[11]}', 
                 f'3 - {competencias.descriptor3[11]}'],
        selected=[],
        inline=True,
    ),
    # },
    # Aprendizaje e innovación
    # "cluster5":{
    "cl5_comp1_descriptors": ui.input_radio_buttons(
        "cl5_comp1_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[12]}', 
                 f'2 - {competencias.descriptor2[12]}', 
                 f'3 - {competencias.descriptor3[12]}'],
        selected=[],
        inline=True,
    ),
    "cl5_comp2_descriptors": ui.input_radio_buttons(
        "cl5_comp2_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[13]}', 
                 f'2 - {competencias.descriptor2[13]}', 
                 f'3 - {competencias.descriptor3[13]}'],
        selected=[],
        inline=True,
    ),
    # },
    # Planeación y Resultados
    # "cluster6":{
    "cl6_comp1_descriptors": ui.input_radio_buttons(
        "cl6_comp1_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[14]}', 
                 f'2 - {competencias.descriptor2[14]}', 
                 f'3 - {competencias.descriptor3[14]}'],
        selected=[],
        inline=True,
    ),
    "cl6_comp2_descriptors": ui.input_radio_buttons(
        "cl6_comp2_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[15]}', 
                 f'2 - {competencias.descriptor2[15]}', 
                 f'3 - {competencias.descriptor3[15]}'],
        selected=[],
        inline=True,
    ),
    "cl6_comp3_descriptors": ui.input_radio_buttons(
        "cl6_comp3_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[16]}', 
                 f'2 - {competencias.descriptor2[16]}', 
                 f'3 - {competencias.descriptor3[16]}'],
        selected=[],
        inline=True,
    ),
    # },
    # Adaptabilidad y Autocontrol
    # "cluster7":{
    "cl7_comp1_descriptors": ui.input_radio_buttons(
        "cl7_comp1_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[17]}', 
                 f'2 - {competencias.descriptor2[17]}', 
                 f'3 - {competencias.descriptor3[17]}'],
        selected=[],
        inline=True,
    ),
    "cl7_comp2_descriptors": ui.input_radio_buttons(
        "cl7_comp2_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[18]}', 
                 f'2 - {competencias.descriptor2[18]}', 
                 f'3 - {competencias.descriptor3[18]}'],
        selected=[],
        inline=True,
    ),
    # },
    # Logro y Ventas
    # "cluster8":{
    "cl8_comp1_descriptors": ui.input_radio_buttons(
        "cl8_comp1_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[19]}', 
                 f'2 - {competencias.descriptor2[19]}', 
                 f'3 - {competencias.descriptor3[19]}'],
        selected=[],
        inline=True,
    ),
    "cl8_comp2_descriptors": ui.input_radio_buttons(
        "cl8_comp2_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[20]}', 
                 f'2 - {competencias.descriptor2[20]}', 
                 f'3 - {competencias.descriptor3[20]}'],
        selected=[],
        inline=True,
    ),
    # },
    # Servicio al Cliente
    # "cluster9":{
    "cl9_comp1_descriptors": ui.input_radio_buttons(
        "cl9_comp1_descriptors",
        "Seleccione la opción que mejor se ajuste:",
        choices=[f'1 - {competencias.descriptor1[21]}', 
                 f'2 - {competencias.descriptor2[21]}', 
                 f'3 - {competencias.descriptor3[21]}'],
        selected=[],
        inline=True,
    ),
}

COMPS = {
    "cl1_comp1": "Toma de Decisiones",
    "cl1_comp2": "Capacidad para Dirigir",
    "cl1_comp3": "Liderazgo",
    "cl1_comp4": "Pensamiento Estratégico",
    "cl2_comp1": "Trabajo en equipo",
    "cl2_comp2": "Integridad/Adhesión a Valores",
    "cl3_comp1": "Desarrollo de Relaciones",
    "cl3_comp2": "Impacto e Influencia",
    "cl3_comp3": "Comunicación Efectiva",
    "cl4_comp1": "Realización de Informes y Reportes",
    "cl4_comp2": "Competencia Técnica",
    "cl4_comp3": "Capacidad de Análsis",
    "cl5_comp1": "Capacidad de Aprendizaje",
    "cl5_comp2": "Capacidad Creativa e de Innovación",
    "cl6_comp1": "Planeación y Organización",
    "cl6_comp2": "Orientación de Resultados",
    "cl6_comp3": "Adhesión a instrucciones y procedimientos",
    "cl7_comp1": "Flexibilidad/Adaptabilidad",
    "cl7_comp2": "Capacidad de Autocontrol",
    "cl8_comp1": "Capacidad de Logro",
    "cl8_comp2": "Habilidad Comercial",
    "cl9_comp1": "Orientación al Servicio"
    }

WEIGHTS = {
    "Líder": 0.4,
    "Partner": 0.15,
    "Autoevaluación":0.2,
    "Cliente interno":0.25
    }