def before_scenario(context, scenario):
    print(f"🚀 Iniciando cenário: {scenario.name}")

def after_scenario(context, scenario):
    print(f"✅ Finalizado cenário: {scenario.name}")
