from datetime import datetime
from dotenv import load_dotenv
import faicons
import os
import numpy as np
from pathlib import Path
import pandas as pd
import plotly.express as px
from shiny import reactive
from shiny.express import input, ui, render
from shiny_validate import InputValidator, check
from shinywidgets import render_plotly
from data_import import competencias, INPUTS, COMPS
from utils import save_to_google_drive, get_worksheet_names, calculate_competence_averages



### Carga dotenv
load_dotenv()
### Obtener ruta de la app.
app_dir = Path(__file__).parent

# Obtener ruta del archivo estilos.
css_path = app_dir / "styles.css"
### Título de la app
ui.include_css(css_path)
ui.page_opts(window_title="Evaluación de Desempeño")


with ui.navset_bar(title="Centro de Ortopedia El Poblado", id="evaluacion_desempeno", bg='#37465d',
                   position='fixed-top', padding="70px"):
    with ui.nav_panel("Evaluación de Desempeño"):
        ### Panel para nombre de evaluador, nombre de evaluado y cargo evalaudo.
        with ui.accordion(id='info_evaluador', open="Información Evaluador"):
            with ui.accordion_panel("Información Evaluador"):
                with ui.card():
                    INPUTS["name_evaluador"]
                    INPUTS["rol_evaluador"]

        with ui.panel_conditional("input.rol_evaluador === 'Autoevaluación'"):
            with ui.accordion(id='info_autoevaluado', open=False):    
                with ui.accordion_panel("Información Autoevaluado"):
                    with ui.card():
                        INPUTS["cargo_evaluado_auto"]

        with ui.panel_conditional("input.rol_evaluador !== 'Autoevaluación'"):
            with ui.accordion(id='info_evaluado', open=False):    
                with ui.accordion_panel("Información Evaluado"):
                    with ui.card():
                        INPUTS["name_evaluado"]
                        INPUTS["cargo_evaluado"]

        ### Panel condicional de directores/analistas para desplegar paneles de competencia de acuerdo al cargo.
        with ui.panel_conditional(f"['Director', 'Analista', 'Médico'].includes(input.cargo_evaluado) || ['Director', 'Analista'].includes(input.cargo_evaluado_auto)"):
            with ui.accordion(id='comp1', open=False):      
                with ui.accordion_panel(f"Competencias - {competencias.clusterName[0]}"):
                    with ui.card():
                        with ui.accordion(id='cluster1', open=False):
                            # Loop through competencies to reduce repetition
                            for i, competencia in enumerate(competencias.competencia[0:4]):
                                with ui.accordion_panel(competencia):
                                    ui.p("Descripción:")
                                    ui.p(competencias.definicion[i], style="text-align: justify;")
                                    with ui.card():
                                        comp_descriptors = f'cl1_comp{i+1}_descriptors'
                                        INPUTS[comp_descriptors]   


        ### Panel condicional de todos los cargos para desplegar paneles de competencia de acuerdo al cargo.
        with ui.panel_conditional(f"['Director', 'Analista', 'Médico', 'Auxiliar'].includes(input.cargo_evaluado) || ['Director', 'Analista', 'Médico', 'Auxiliar'].includes(input.cargo_evaluado_auto)"):
            with ui.accordion(id='comp2', open=False, style='margin-top:-26px'):
                # Obtener clusters únicos
                clusters = competencias["cluster"].unique()
                clusters = clusters[1:]
                
                # Crear la UI basada en clusters, competencias y descriptores
                for cluster_id in clusters:
                    cluster_data = competencias[competencias["cluster"] == cluster_id].reset_index()
                    cluster_name = cluster_data["clusterName"].iloc[0]
                    cluster_num_comps = cluster_data.shape[0]
                
                    # Crear un accordion panel para cada cluster.
                    if pd.notna(cluster_data['descriptor1'][0]):
                        with ui.accordion_panel(f"Competencias - {cluster_name}"):
                            with ui.card():
                                with ui.accordion(id=f'cluster{cluster_id}', open=False):
                                    # Crear un accordion panel para cada competencia en el cluster
                                    for comp in range(1, cluster_num_comps+1):
                                        if pd.notna(cluster_data['descriptor1'][comp-1]):
                                            competencia_name = cluster_data.competencia[comp-1]
                                            definicion = cluster_data.definicion[comp-1]
                                            with ui.accordion_panel(competencia_name):
                                                ui.p("Descripción:", style="font-weight: bold;")
                                                ui.p(definicion, style="text-align: justify;")
                                                # Create cards para cada descriptor (si no son NaN)
                                                with ui.card():
                                                    INPUTS[f"cl{cluster_id}_comp{comp}_descriptors"]

        ui.p()
        # Botón para enviar formulario.
        ui.div(
            ui.input_action_button("enviar", "Enviar", class_="btn btn-primary"),
            class_="d-flex justify-content-end",
        )
        

    with ui.nav_panel(title="Análisis de Desempeño"):
        
        # valid username and password
        valid_username = os.getenv("VALID_USERNAME")
        valid_password = os.getenv("VALID_PASSWORD")

        # Reactive value to track login status
        login_status = reactive.value(False)
        # Hidden input to sync login status with the frontend
        ui.div(ui.input_text("login_status", None, value=""), style="display:none;")

        @render.ui
        def login_form():
            if not login_status():
                return ui.div(
                    ui.input_text("username", "Usuario"),
                    ui.input_password("password", "Contraseña"),
                    ui.input_action_button("login", "Ingresar"),
                )
            else:
                return ui.div(style='display:none')

        # Handle the login button click
        @reactive.effect
        @reactive.event(input.login)
        def handle_login():
            if input.username() == valid_username and input.password() == valid_password:
                login_status.set(True)
                ui.update_text("login_status", value="logged_in")
            else:
                login_status.set(False)
                ui.update_text("login_status", value="")
                ui.modal_show(ui.modal("Ingrese un usuario y/o contraseña válidos.",
                              footer=ui.modal_button("Cerrar", id="close_modal")))

        
        with ui.panel_conditional(f"['logged_in'].includes(input.login_status)"):    
            with ui.layout_sidebar(style="margin-right: -10%; margin-left=0px; padding-left=0px;"):
                with ui.sidebar(bg="#37465d", style="color: white;",
                                border=None):  
                    names = get_worksheet_names()
                    ui.input_select(
                        "select_employee",
                        "Evaluado",
                        names,
                        selected=names[0]
                    )

                    ui.input_date(
                        "date_filter",
                        "Fecha evaluación",
                        format="dd-mm-yyyy",
                    )

                with ui.accordion(open=False):
                    with ui.accordion_panel("Nivel de Desarrollo por Competencia"):
                        with ui.card():
                            @render_plotly
                            def plot_competences():
                                try:
                                    df_subset = select_data()
                                    df_subset.rename(columns=COMPS, inplace=True)
                                    df_melted = pd.melt(df_subset, var_name='Competencia', value_name='Nivel de Desarrollo')
                                    df_melted['Nivel de Desarrollo'] = (df_melted['Nivel de Desarrollo'] / 3)*100
                                    df_melted['Nivel de Desarrollo'] = df_melted['Nivel de Desarrollo'].round(2)
                                    # Drop NaN values (which represent empty entries)
                                    df_melted.dropna(subset=['Nivel de Desarrollo'], inplace=True)
                                    # Maintain the original order of the competencies
                                    competence_order = df_melted['Competencia'].unique().tolist()  # Get the order of non-NaN competencies
                                    return px.bar(df_melted,
                                                y='Competencia',
                                                x='Nivel de Desarrollo',
                                                text='Nivel de Desarrollo',
                                                range_x=[30, 100],
                                                category_orders={'Competencia': competence_order},
                                                color_discrete_sequence=['#4F7CAC'] ,
                                                color='Nivel de Desarrollo',
                                                color_continuous_scale='Teal',                         
                                                ).update_traces(
                                                    textposition='outside',
                                                ).update_layout(
                                                    xaxis_title='Nivel de desarrollo (%)',
                                                    yaxis_title='',
                                                    coloraxis_showscale=False,
                                                    margin=dict(l=0)
                                                    ) 

                                except:
                                    comps = list(COMPS.values())
                                    df_empty = pd.DataFrame({"Competencia": comps, "Nivel de Desarrollo": 0.0})
                                    return px.bar(df_empty,
                                                y='Competencia',
                                                x='Nivel de Desarrollo',
                                                text='Nivel de Desarrollo',
                                                range_x=[30, 100],
                                                category_orders={'Competencia': competence_order},
                                                color_discrete_sequence=['#4F7CAC'] ,
                                                color='Nivel de Desarrollo',
                                                color_continuous_scale='Teal',                         
                                                ).update_traces(
                                                    textposition='outside',
                                                ).update_layout(
                                                    xaxis_title='Nivel de desarrollo (%)',
                                                    yaxis_title='',
                                                    coloraxis_showscale=False,
                                                    margin=dict(l=0)
                                                    ) 

                with ui.layout_columns():
                    with ui.value_box(
                        showcase=faicons.icon_svg("list-check"),
                        theme="orange",
                        showcase_layout="left center",
                        full_screen=False
                        ):
                        "Nivel de Desarrollo Total:"

                        @render.ui
                        def total():
                            try:
                                df_subset = select_data()
                                # Calculate the average for each competence
                                avg_df = df_subset.mean().reset_index()  # Reset index to turn it into a DataFrame
                                avg_df.columns = ['Competencia', 'Nivel de Desarrollo']  # Rename columns for better readability

                                # Remove rows where the average is NaN (if any)
                                avg_df.dropna(subset=['Nivel de Desarrollo'], inplace=True)         
                                avg_total = avg_df['Nivel de Desarrollo'].mean()

                                if pd.notna(avg_total):
                                    return f'{(avg_total / 3) * 100:.2f} %'
                                else:
                                    return f''
                            except:
                                return f''

                    with ui.value_box(
                        showcase=faicons.icon_svg("check-double"),
                        theme="light",
                        showcase_layout="left center",
                        full_screen=False
                        ):
                        "Competencia para sostener: "
                    
                        @render.ui
                        def best_competence():
                            try:
                                df_subset = select_data()
                                # Calculate the average for each competence
                                df_subset.rename(columns=COMPS, inplace=True)
                                df_melted = pd.melt(df_subset, var_name='Competencia', value_name='Nivel de Desarrollo')
                                best_competence = df_melted[df_melted['Nivel de Desarrollo'] == df_melted['Nivel de Desarrollo'].max()]
                                best_competence_score = df_melted['Nivel de Desarrollo'].max()
                
                                return f'{best_competence["Competencia"].values[0]}\n {(best_competence_score / 3) * 100:.2f} %'
                            except:
                                return f''

                    with ui.value_box(
                        showcase=faicons.icon_svg("stairs"),
                        theme="secondary",
                        showcase_layout="left center",
                        full_screen=False
                        ):
                        "Competencia para fortalecer: "

                        @render.ui
                        def worst_competence():
                            try:
                                df_subset = select_data()
                                # Calculate the average for each competence
                                df_subset.rename(columns=COMPS, inplace=True)
                                df_melted = pd.melt(df_subset, var_name='Competencia', value_name='Nivel de Desarrollo')
                                best_competence = df_melted[df_melted['Nivel de Desarrollo'] == df_melted['Nivel de Desarrollo'].min()]
                                best_competence_score = df_melted['Nivel de Desarrollo'].min()

                                return f'{best_competence["Competencia"].values[0]}\n {(best_competence_score / 3) * 100:.2f} %'
                            except:
                                return f''





def select_data():
    return calculate_competence_averages(input.select_employee(), input.date_filter())

# Requerido para que InputValidator funcione en Express
input_validator = None
@reactive.effect
def _():
# Agregar validaciones a cada input según sea neceario.
    global input_validator
    input_validator = InputValidator()
    
    # Core fields that should always be required
    input_validator.add_rule("name_evaluador", check.required(message="Campo requerido"))
    input_validator.add_rule("rol_evaluador", check.required(message="Campo requerido"))

    # Conditional rule based on rol_evaluador
    if input.rol_evaluador() == "Autoevaluación":
        input_validator.add_rule("cargo_evaluado_auto", check.required(message="Campo requerido"))
    else:
        input_validator.add_rule("name_evaluado", check.required(message="Campo requerido"))
        input_validator.add_rule("cargo_evaluado", check.required(message="Campo requerido"))

# Efecto y mensaje de salida cuando se envié el fomrulario usando Enviar.
@reactive.effect
@reactive.event(input.enviar)
def save_to_csv():
    
    input_validator.enable()
    if not input_validator.is_valid(): 
        ui.modal_show(ui.modal("Error: Entradas inválidas. Por favor revise sus respuestas e intente nuevamente.",
                      footer=ui.modal_button("Cerrar", id="close_modal")))
        return

    column_names = list(INPUTS.keys())
    column_names.append("created_at")
    column_names.append("updated_at")
    responses = app_dir / "responses.csv"

    # Initialize the DataFrame if it doesn't exist yet


    if not responses.exists():
        df = pd.DataFrame(columns=column_names)
        df.to_csv(responses, index=False)

    try:
        # Collect input values and validate each one
        input_data = {}
        for k in INPUTS.keys():
            if k in input:  # Check if the input exists
                try:
                    value = input[k]()  # Fetch the input value
                    if value is None:
                        pass
                    elif "_descriptors" in k:
                        value = value[0]
                    
                        # print(f"Warning: Input '{k}' is None.")
                    input_data[k] = value
                except Exception as e:
                    # print(f"Error accessing input '{k}': {e}")
                    ui.modal_show(ui.modal(f"Error accediendo a la entrada '{k}':{e}."))
                    return
            else:
                # Input does not exist, you can choose to omit it or handle it differently
                print(f"Notice: Input '{k}' is not present in the form.")

        current_timestamp = datetime.now().isoformat()
        input_data["created_at"] = current_timestamp
        input_data["updated_at"] = current_timestamp
        
        input_data['name_evaluador'] = input_data['name_evaluador'].title()
        if input_data['rol_evaluador'] != 'Autoevaluación':
            input_data['name_evaluado'] = input_data['name_evaluado'].title()

        # Create a DataFrame row with the collected input data
        df_row = pd.DataFrame([input_data])
        if input_data['rol_evaluador'] == 'Autoevaluación':
            save_to_google_drive(df_row, input_data['name_evaluador'])
        else:
            save_to_google_drive(df_row, input_data['name_evaluado'])
        # Show success message
        ui.modal_show(ui.modal("Evaluación enviada, ¡Gracias!",
                               footer=ui.modal_button("Cerrar", id="close_modal")))


    except Exception as e:
        # Log the error and show an error message.
        # print(type(e))
        # print(f"Error saving to CSV: {e}")
        ui.modal_show(ui.modal("Error al guardar los datos. Inténtelo de nuevo."))


@reactive.effect
@reactive.event(input.enviar)
def reset_inputs():
    # Reset each input to its default state
     for key in INPUTS.keys():
        # Adjust this to match your input types and desired default values
        if "name" in key:  # Example condition for text inputs
           ui.update_text(
               key,
               value=""
           )  # Reset text inputs to empty
        elif "rol_evaluador" in key or "cargo" in key:  # Example for a dropdown or radio button
            ui.update_select(
                key,
                selected=""
            )
        else:
            ui.update_radio_buttons(
                key,
                selected=[]
            )