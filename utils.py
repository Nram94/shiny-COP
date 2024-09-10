import pandas as pd
from shiny import session
from data_import import INPUTS

def collect_inputs():
    # Initialize an empty list to store the input data
    data = []

    # Collect the main evaluator's details
    evaluator_data = {
        "field": "name_evaluador",
        "value": INPUTS["name_evaluador"].value,
    }
    data.append(evaluator_data)

    evaluator_role = {
        "field": "rol_evaluador",
        "label": INPUTS["rol_evaluador"].label,
        "value": INPUTS["rol_evaluador"].value,
    }
    data.append(evaluator_role)

    evaluated_name = {
        "field": "name_evaluado",
        "label": INPUTS["name_evaluado"].label,
        "value": INPUTS["name_evaluado"].value,
    }
    data.append(evaluated_name)

    cargo_evaluado = {
        "field": "cargo_evaluado",
        "label": INPUTS["cargo_evaluado"].label,
        "value": INPUTS["cargo_evaluado"].value,
    }
    data.append(cargo_evaluado)

    cargo_evaluado_auto = {
        "field": "cargo_evaluado_auto",
        "label": INPUTS["cargo_evaluado_auto"].label,
        "value": INPUTS["cargo_evaluado_auto"].value,
    }
    data.append(cargo_evaluado_auto)

    # Iterate through each cluster to collect their descriptor values
    for cluster_name, cluster_inputs in INPUTS.items():
        if cluster_name.startswith("cluster"):
            for descriptor_name, descriptor_input in cluster_inputs.items():
                descriptor_data = {
                    "field": descriptor_name,
                    "label": descriptor_input.label,
                    "value": descriptor_input.value,
                }
                data.append(descriptor_data)

    # Convert the collected data into a DataFrame
    df = pd.DataFrame(data)
    return df
