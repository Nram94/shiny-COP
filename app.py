from datetime import datetime
from pathlib import Path
import pandas as pd
import plotly.express as px
from shiny import reactive
from shiny.express import input, ui, render
from shiny_validate import InputValidator, check
from shinywidgets import render_plotly
from data_import import competencias, INPUTS, WEIGHTS, COMPS
from utils import save_to_google_drive, get_worksheet_names, calculate_competence_averages


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
                            for i, competencia in enumerate(competencias.competencia[0:2]):
                                with ui.accordion_panel(competencia):
                                    ui.p("Descripción:")
                                    ui.p(competencias.definicion[i], style="text-align: justify;")
                                    with ui.card():
                                        # Loop through descriptors for each competencia
                                        for j in range(1, 4):
                                            descriptor_id = f'cl1_comp{i+1}_descriptor{j}'
                                            INPUTS[descriptor_id]   

        ### Panel condicional de todos los cargos para desplegar paneles de competencia de acuerdo al cargo.
        with ui.panel_conditional(f"['Director', 'Analista', 'Médico', 'Auxiliar'].includes(input.cargo_evaluado) || ['Director', 'Analista', 'Auxiliar'].includes(input.cargo_evaluado_auto)"):
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
                    with ui.accordion_panel(f"Competencias - {cluster_name}"):
                        with ui.card():
                            with ui.accordion(id=f'cluster{cluster_id}', open=False):
                                # Crear un accordion panel para cada competencia en el cluster
                                for comp in range(1, cluster_num_comps+1):
                                    competencia_name = cluster_data.competencia[comp-1]
                                    definicion = cluster_data.definicion[comp-1]
                                    if pd.notna(cluster_data['descriptor1'][comp-1]):
                                        with ui.accordion_panel(competencia_name):
                                            ui.p("Descripción:", style="font-weight: bold;")
                                            ui.p(definicion, style="text-align: justify;")
                                            # Create cards para cada descriptor (si no son NaN)
                                            with ui.card():
                                                for desc in range(1, 4):
                                                    INPUTS[f"cl{cluster_id}_comp{comp}_descriptor{desc}"]

        ui.p()
        # Botón para enviar formulario.
        ui.div(
            ui.input_action_button("enviar", "Enviar", class_="btn btn-primary"),
            class_="d-flex justify-content-end",
        )

    with ui.nav_panel("Análisis de Desempeño"):
        with ui.layout_sidebar():
            with ui.sidebar(bg="#37465d", style="color: white; border: none;", 
                border=None):  

                # ui.input_slider("mass", "Max Body Mass", 200, 8000, 6000)
                # ui.input_checkbox_group(
                #     "species",
                #     "Species",
                #     ["Adelie", "Chinstrap", "Gentoo"],
                #     selected=["Adelie", "Chinstrap", "Gentoo"],
                    
                # )
                names = get_worksheet_names()
                ui.input_select(
                    "select_employee",
                    "Evaluado",
                    names,
                    selected=names[0]
                )
                

            with ui.layout_columns():
                with ui.card():
                    @render_plotly
                    def plot():
                        try:
                            df_subset = select_data()
                            df_melted = pd.melt(df_subset, var_name='Competencia', value_name='Nivel de Desarrollo')
                            df_melted['Nivel de Desarrollo'] = df_melted['Nivel de Desarrollo'].round(2)

                            return px.bar(df_melted,
                                        title='Nivel de Desarrollo por Competencia', 
                                        y='Competencia',
                                        x='Nivel de Desarrollo',
                                        text='Nivel de Desarrollo',
                                        range_x=[0, 3],
                                        ).update_traces(
                                            textposition='outside',

                                        ).update_layout(yaxis_title='')
                        except:
                            comps = list(COMPS.values())
                            df_empty = pd.DataFrame({"Competencia": comps, "Nivel de Desarrollo": 0.0})
                            return px.bar(df_empty,
                                        title='Nivel de Desarrollo por Competencia', 
                                        y='Competencia',
                                        x='Nivel de Desarrollo',
                                        text='Nivel de Desarrollo',
                                        range_x=[0, 3],
                                        ).update_traces(
                                            textposition='outside',

                                        ).update_layout(yaxis_title='')
                
                    @render.data_frame
                    def render_weights():
                        weights_df = pd.DataFrame(list(WEIGHTS.items()), columns=['Rol Evaluador', 'Peso(%)'])
                        weights_df['Peso(%)'] = weights_df['Peso(%)'] * 100
                        return render.DataGrid(weights_df)


                # with ui.card(): 
                #     "table"
                #     @render.data_frame
                #     def data_f():
                #         df_subset_table = load_from_google_drive()
                #         return df_subset_table.head() 


# Requerido para que InputValidator funcione en Express
input_validator = None


def select_data():
    return calculate_competence_averages(input.select_employee())

@reactive.effect
def _():
# Agregar validaciones a cada input según sea neceario.
    global input_validator
    input_validator = InputValidator()
    input_validator.add_rule("name_evaluador", check.required(message="Campo requerido"))
    input_validator.add_rule("rol_evaluador", check.required(message="Campo requerido"))
    if input.rol_evaluador() == "Autoevaluación":
        input_validator.add_rule("cargo_evaluado_auto", check.required(message="Campo requerido")) 
    else:
        input_validator.add_rule("name_evaluado", check.required(message="Campo requerido"))
        input_validator.add_rule("cargo_evaluado", check.required(message="Campo requerido"))

    # if input.cargo_evaluado() == "Auxiliar" or input.cargo_evaluado_auto() == "Auxiliar":
    #     for key, input_widget in INPUTS.items():
    #         if not("cl1" in key):
    #             if ("descriptor" in key):
    #                 input_validator.add_rule(key, check.required(message="Campo requerido"))    
    # else:
    #     for key, input_widget in INPUTS.items():
    #         if ("descriptor" in key):
    #             input_validator.add_rule(key, check.required(message="Campo requerido")) 


# Efecto y mensaje de salida cuando se envié el fomrulario usando Enviar.
@reactive.effect
@reactive.event(input.enviar)
def save_to_csv():
    input_validator.enable()
    if not input_validator.is_valid():
        ui.modal_show(ui.modal("Error: Entradas inválidas. Por favor revise sus respuestas e intente nuevamente."))
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
                        # print(f"Warning: Input '{k}' is None.")
                    input_data[k] = value
                except Exception as e:
                    # print(f"Error accessing input '{k}': {e}")
                    ui.modal_show(ui.modal(f"Error accediendo a la entrada '{k}'."))
                    return
            else:
                # Input does not exist, you can choose to omit it or handle it differently
                print(f"Notice: Input '{k}' is not present in the form.")

        current_timestamp = datetime.now().isoformat()
        input_data["created_at"] = current_timestamp
        input_data["updated_at"] = current_timestamp

        # Create a DataFrame row with the collected input data
        df_row = pd.DataFrame([input_data])
        if input_data['rol_evaluador'] == 'Autoevaluación':
            save_to_google_drive(df_row, input_data['name_evaluador'])
        else:
            save_to_google_drive(df_row, input_data['name_evaluado'])
        # Show success message
        ui.modal_show(ui.modal("Evaluación enviada, ¡Gracias!"))


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