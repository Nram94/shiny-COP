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


### Esquema de inputs de UI.
INPUTS = {
    "name_evaluador": ui.input_text("name_evaluador", "Ingrese su nombre completo:"),
    "rol_evaluador":ui.input_select(
        "rol_evaluador",
        "Rol del evaluador",
        choices = ["", "Líder", "Partner", "Cliente Interno", "Autoevaluación"]
        ),
    "name_evaluado": ui.input_text("name_evaluado", 
                                   "Ingrese nombre completo de la persona a evaluar:"),
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
    "cl1_comp1_descriptor1": ui.input_radio_buttons(
        "cl1_comp1_descriptor1",
        competencias.descriptor1[0],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl1_comp1_descriptor2": ui.input_radio_buttons(
        "cl1_comp1_descriptor2",
        competencias.descriptor2[0],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl1_comp1_descriptor3": ui.input_radio_buttons(
        "cl1_comp1_descriptor3",
        competencias.descriptor3[0],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl1_comp2_descriptor1": ui.input_radio_buttons(
        "cl1_comp2_descriptor1",
        competencias.descriptor1[1],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl1_comp2_descriptor2": ui.input_radio_buttons(
        "cl1_comp2_descriptor2",
        competencias.descriptor2[1],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl1_comp2_descriptor3": ui.input_radio_buttons(
        "cl1_comp2_descriptor3",
        competencias.descriptor3[1],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    # Equipo e Integridad
    # "cluster2":{
    "cl2_comp1_descriptor1": ui.input_radio_buttons(
        "cl2_comp1_descriptor1",
        competencias.descriptor1[2],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl2_comp1_descriptor2": ui.input_radio_buttons(
        "cl2_comp1_descriptor2",
        competencias.descriptor2[2],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl2_comp1_descriptor3": ui.input_radio_buttons(
        "cl2_comp1_descriptor3",
        competencias.descriptor3[2],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl2_comp2_descriptor1": ui.input_radio_buttons(
        "cl2_comp2_descriptor1",
        competencias.descriptor1[3],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl2_comp2_descriptor2": ui.input_radio_buttons(
        "cl2_comp2_descriptor2",
        competencias.descriptor2[3],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl2_comp2_descriptor3": ui.input_radio_buttons(
        "cl2_comp2_descriptor3",
        competencias.descriptor3[3],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    # },
    # Relaciones e Influencia
    # "cluster3":{
    "cl3_comp1_descriptor1": ui.input_radio_buttons(
        "cl3_comp1_descriptor1",
        competencias.descriptor1[4],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl3_comp1_descriptor2": ui.input_radio_buttons(
        "cl3_comp1_descriptor2",
        competencias.descriptor2[4],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl3_comp1_descriptor3": ui.input_radio_buttons(
        "cl3_comp1_descriptor3",
        competencias.descriptor3[4],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl3_comp2_descriptor1": ui.input_radio_buttons(
        "cl3_comp2_descriptor1",
        competencias.descriptor1[5],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl3_comp2_descriptor2": ui.input_radio_buttons(
        "cl3_comp2_descriptor2",
        competencias.descriptor2[5],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl3_comp2_descriptor3": ui.input_radio_buttons(
        "cl3_comp2_descriptor3",
        competencias.descriptor3[5],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl3_comp3_descriptor1": ui.input_radio_buttons(
        "cl3_comp3_descriptor1",
        competencias.descriptor1[6],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl3_comp3_descriptor2": ui.input_radio_buttons(
        "cl3_comp3_descriptor2",
        competencias.descriptor2[6],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl3_comp3_descriptor3": ui.input_radio_buttons(
        "cl3_comp3_descriptor3",
        competencias.descriptor3[6],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    # },
    # Análisis y Reportes
    # "cluster4":{
    "cl4_comp1_descriptor1": ui.input_radio_buttons(
        "cl4_comp1_descriptor1",
        competencias.descriptor1[7],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl4_comp1_descriptor2": ui.input_radio_buttons(
        "cl4_comp1_descriptor2",
        competencias.descriptor2[7],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl4_comp1_descriptor3": ui.input_radio_buttons(
        "cl4_comp1_descriptor3",
        competencias.descriptor3[7],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl4_comp2_descriptor1": ui.input_radio_buttons(
        "cl4_comp2_descriptor1",
        competencias.descriptor1[8],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl4_comp2_descriptor2": ui.input_radio_buttons(
        "cl4_comp2_descriptor2",
        competencias.descriptor2[8],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl4_comp2_descriptor3": ui.input_radio_buttons(
        "cl4_comp2_descriptor3",
        competencias.descriptor3[8],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl4_comp3_descriptor1": ui.input_radio_buttons(
        "cl4_comp3_descriptor1",
        competencias.descriptor1[9],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl4_comp3_descriptor2": ui.input_radio_buttons(
        "cl4_comp3_descriptor2",
        competencias.descriptor2[9],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl4_comp3_descriptor3": ui.input_radio_buttons(
        "cl4_comp3_descriptor3",
        competencias.descriptor3[9],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    # },
    # Aprendizaje e innovación
    # "cluster5":{
    "cl5_comp1_descriptor1": ui.input_radio_buttons(
        "cl5_comp1_descriptor1",
        competencias.descriptor1[10],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl5_comp1_descriptor2": ui.input_radio_buttons(
        "cl5_comp1_descriptor2",
        competencias.descriptor2[10],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl5_comp1_descriptor3": ui.input_radio_buttons(
        "cl5_comp1_descriptor3",
        competencias.descriptor3[10],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl5_comp2_descriptor1": ui.input_radio_buttons(
        "cl5_comp2_descriptor1",
        competencias.descriptor1[11],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl5_comp2_descriptor2": ui.input_radio_buttons(
        "cl5_comp2_descriptor2",
        competencias.descriptor2[11],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl5_comp2_descriptor3": ui.input_radio_buttons(
        "cl5_comp2_descriptor3",
        competencias.descriptor3[11],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl5_comp3_descriptor1": ui.input_radio_buttons(
        "cl5_comp3_descriptor1",
        competencias.descriptor1[12],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl5_comp3_descriptor2": ui.input_radio_buttons(
        "cl5_comp3_descriptor2",
        competencias.descriptor2[12],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl5_comp3_descriptor3": ui.input_radio_buttons(
        "cl5_comp3_descriptor3",
        competencias.descriptor3[12],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    # },
    # Planeación y Resultados
    # "cluster6":{
    "cl6_comp1_descriptor1": ui.input_radio_buttons(
        "cl6_comp1_descriptor1",
        competencias.descriptor1[13],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl6_comp1_descriptor2": ui.input_radio_buttons(
        "cl6_comp1_descriptor2",
        competencias.descriptor2[13],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl6_comp1_descriptor3": ui.input_radio_buttons(
        "cl6_comp1_descriptor3",
        competencias.descriptor3[13],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl6_comp2_descriptor1": ui.input_radio_buttons(
        "cl6_comp2_descriptor1",
        competencias.descriptor1[14],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl6_comp2_descriptor2": ui.input_radio_buttons(
        "cl6_comp2_descriptor2",
        competencias.descriptor2[14],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl6_comp2_descriptor3": ui.input_radio_buttons(
        "cl6_comp2_descriptor3",
        competencias.descriptor3[14],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl6_comp3_descriptor1": ui.input_radio_buttons(
        "cl6_comp3_descriptor1",
        competencias.descriptor1[15],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl6_comp3_descriptor2": ui.input_radio_buttons(
        "cl6_comp3_descriptor2",
        competencias.descriptor2[15],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl6_comp3_descriptor3": ui.input_radio_buttons(
        "cl6_comp3_descriptor3",
        competencias.descriptor3[15],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    # },
    # Adaptabilidad y Autocontrol
    # "cluster7":{
    "cl7_comp1_descriptor1": ui.input_radio_buttons(
        "cl7_comp1_descriptor1",
        competencias.descriptor1[16],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl7_comp1_descriptor2": ui.input_radio_buttons(
        "cl7_comp1_descriptor2",
        competencias.descriptor2[16],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl7_comp1_descriptor3": ui.input_radio_buttons(
        "cl7_comp1_descriptor3",
        competencias.descriptor3[16],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl7_comp2_descriptor1": ui.input_radio_buttons(
        "cl7_comp2_descriptor1",
        competencias.descriptor1[17],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl7_comp2_descriptor2": ui.input_radio_buttons(
        "cl7_comp2_descriptor2",
        competencias.descriptor2[17],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl7_comp2_descriptor3": ui.input_radio_buttons(
        "cl7_comp2_descriptor3",
        competencias.descriptor3[17],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    # },
    # Logro y Ventas
    # "cluster8":{
    "cl8_comp1_descriptor1": ui.input_radio_buttons(
        "cl8_comp1_descriptor1",
        competencias.descriptor1[18],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl8_comp1_descriptor2": ui.input_radio_buttons(
        "cl8_comp1_descriptor2",
        competencias.descriptor2[18],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl8_comp1_descriptor3": ui.input_radio_buttons(
        "cl8_comp1_descriptor3",
        competencias.descriptor3[18],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
),
    "cl8_comp2_descriptor1": ui.input_radio_buttons(
        "cl8_comp2_descriptor1",
        competencias.descriptor1[19],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl8_comp2_descriptor2": ui.input_radio_buttons(
        "cl8_comp2_descriptor2",
        competencias.descriptor2[19],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl8_comp2_descriptor3": ui.input_radio_buttons(
        "cl8_comp2_descriptor3",
        competencias.descriptor3[19],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    # },
    # Servicio al Cliente
    # "cluster9":{
    "cl9_comp1_descriptor1": ui.input_radio_buttons(
        "cl9_comp1_descriptor1",
        competencias.descriptor1[20],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl9_comp1_descriptor2": ui.input_radio_buttons(
        "cl9_comp1_descriptor2",
        competencias.descriptor2[20],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    "cl9_comp1_descriptor3": ui.input_radio_buttons(
        "cl9_comp1_descriptor3",
        competencias.descriptor3[20],
        choices=[1, 2, 3],
        selected=[],
        inline=True,
    ),
    # },
}

COMPS = {
    "cl1_comp1": "Toma de Decisiones",
    "cl1_comp2": "Capacidad para Dirigir",
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
    "cl5_comp3": "Pensamiento Estratégico",
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