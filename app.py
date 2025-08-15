from modules import ui, import_data, plots




df = import_data.get_data()

filtered_df = ui.ui(df)

plots.plots(filtered_df)

    
