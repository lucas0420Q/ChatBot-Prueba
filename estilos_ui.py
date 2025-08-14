"""
Archivo centralizado de estilos CSS para el Asistente Virtual QA
Contiene todos los estilos reutilizables para mantener consistencia visual
"""

# Estilos principales del AsistenteVirtualQA
ESTILOS_ASISTENTE_PRINCIPAL = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #0B1D4A, stop: 1 #1F2A56);
}

#headerFrame {
    background: transparent;
    border: none;
}

#botIcon {
    font-size: 36px;
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #6366F1);
    border-radius: 35px;
    color: white;
    font-weight: bold;
}

#mainTitle {
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin: 0px;
}

#subtitle {
    font-size: 16px;
    color: #94A3B8;
    margin: 0px;
}

#chatFrame {
    background: #141F3C;
    border-radius: 20px;
    border: 2px solid #4C5BFF;
}

#areaChat {
    background: #141F3C;
    border: none;
    border-radius: 15px;
    padding: 20px;
    font-size: 14px;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #ffffff;
}

#areaChat QScrollBar:vertical {
    background: #1B243A;
    width: 12px;
    border-radius: 6px;
    margin: 0px;
}

#areaChat QScrollBar::handle:vertical {
    background: #4C5BFF;
    border-radius: 6px;
    min-height: 25px;
}

#areaChat QScrollBar::handle:vertical:hover {
    background: #6366F1;
}

#inputFrame {
    background: transparent;
    border: none;
}

#entradaTexto {
    background: #1B243A;
    color: #ffffff;
    border: 2px solid #4C5BFF;
    border-radius: 15px;
    padding: 15px 20px;
    font-size: 16px;
    font-family: 'Segoe UI', Arial, sans-serif;
    line-height: 1.5;
    selection-background-color: #4C5BFF;
}

#entradaTexto:focus {
    border: 2px solid #6366F1;
    background: #1E2A40;
    outline: none;
}

#entradaTexto QScrollBar:vertical {
    background: #1B243A;
    width: 10px;
    border-radius: 5px;
    margin: 2px;
    border: 1px solid #4C5BFF;
}

#entradaTexto QScrollBar::handle:vertical {
    background: #4C5BFF;
    border-radius: 5px;
    min-height: 25px;
    margin: 1px;
}

#entradaTexto QScrollBar::handle:vertical:hover {
    background: #6366F1;
}

#entradaTexto QScrollBar::add-line:vertical,
#entradaTexto QScrollBar::sub-line:vertical {
    height: 0px;
}

#attachButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #6366F1);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    padding: 8px 15px;
    min-width: 100px;
}

#attachButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #6366F1, stop: 1 #7C3AED);
}

#clearButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #EF4444, stop: 1 #DC2626);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    padding: 8px 15px;
    min-width: 100px;
}

#clearButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #F87171, stop: 1 #EF4444);
}

#archivosWidget {
    background: #1B243A;
    border: 2px solid #4C5BFF;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
}

#archivoFrame {
    background: #2D3748;
    border: 1px solid #4C5BFF;
    border-radius: 8px;
    margin: 2px;
    padding: 5px;
}

#archivoFrame:hover {
    background: #374151;
    border: 1px solid #6366F1;
}

#archivoLabel {
    color: #E2E8F0;
    font-size: 14px;
    font-weight: bold;
    padding: 2px 5px;
}

#eliminarArchivoBtn {
    background: #EF4444;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}

#eliminarArchivoBtn:hover {
    background: #F87171;
}

#sendButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #2EC877, stop: 1 #10B981);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    padding: 8px 15px;
    min-width: 100px;
}

#sendButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #34D399, stop: 1 #059669);
}

#buttonsFrame {
    background: transparent;
}

#helpButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #5A47F3, stop: 1 #7C3AED);
    color: white;
    border: none;
    border-radius: 15px;
    font-size: 16px;
    font-weight: bold;
    padding: 15px 25px;
}

#helpButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #7C3AED, stop: 1 #A855F7);
}

#historyButton, #advancedButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #1E3058, stop: 1 #2D3748);
    color: white;
    border: 2px solid #4C5BFF;
    border-radius: 15px;
    font-size: 16px;
    font-weight: bold;
    padding: 15px 25px;
}

#historyButton:hover, #advancedButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #6366F1);
    border: 2px solid #6366F1;
}

#footerFrame {
    background: transparent;
}

#statusLabel {
    color: #94A3B8;
    font-size: 14px;
    font-weight: normal;
}
"""

# Estilos para el panel QA avanzado
ESTILOS_PANEL_QA = """
QDialog {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #0B1D4A, stop: 1 #1F2A56);
    color: #FFFFFF;
    font-family: 'Segoe UI', Arial, sans-serif;
}

#tituloPanel {
    font-size: 28px;
    font-weight: bold;
    color: #FFFFFF;
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #6366F1);
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #FFFFFF;
    margin: 10px;
}

#botonCategoria {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #1E3058, stop: 1 #2D3748);
    color: #FFFFFF;
    border: 2px solid #4C5BFF;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    padding: 15px 20px;
    text-align: left;
    min-height: 60px;
}

#botonCategoria:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #6366F1);
    border: 2px solid #FFFFFF;
}

#botonHerramienta {
    background: #2D3748;
    color: #FFFFFF;
    border: 1px solid #4C5BFF;
    border-radius: 8px;
    padding: 12px 15px;
    text-align: left;
    font-size: 14px;
    min-height: 40px;
}

#botonHerramienta:hover {
    background: #4C5BFF;
    color: #FFFFFF;
}

#botonNotion {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #2EC877, stop: 1 #10B981);
    color: white;
    border: none;
    border-radius: 15px;
    font-size: 16px;
    font-weight: bold;
    padding: 15px 25px;
    min-width: 180px;
}

#botonNotion:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #34D399, stop: 1 #059669);
}

#botonExportNotion {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #8B5CF6, stop: 1 #7C3AED);
    color: white;
    border: none;
    border-radius: 15px;
    font-size: 16px;
    font-weight: bold;
    padding: 15px 25px;
    min-width: 180px;
}

#botonExportNotion:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #A855F7, stop: 1 #9333EA);
}

#botonCerrar {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #EF4444, stop: 1 #DC2626);
    color: white;
    border: none;
    border-radius: 15px;
    font-size: 16px;
    font-weight: bold;
    padding: 15px 25px;
    min-width: 120px;
}

#botonCerrar:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #F87171, stop: 1 #EF4444);
}

QMessageBox {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #0B1D4A, stop: 1 #1F2A56);
    color: #FFFFFF;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
    border: 2px solid #4C5BFF;
    border-radius: 15px;
}

QMessageBox QLabel {
    color: #FFFFFF;
    font-size: 14px;
    background: transparent;
    padding: 10px;
}

QMessageBox QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #6366F1);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    padding: 10px 20px;
    min-width: 80px;
    margin: 5px;
}

QMessageBox QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #6366F1, stop: 1 #7C3AED);
}
"""

# Estilos para diálogos de configuración
ESTILOS_CONFIGURACION = """
QDialog {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #0B1D4A, stop: 1 #1F2A56);
    color: #FFFFFF;
    font-family: 'Segoe UI', Arial, sans-serif;
}

#tituloConfig {
    font-size: 24px;
    font-weight: bold;
    color: #FFFFFF;
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #6366F1);
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #FFFFFF;
    margin: 10px;
}

QLineEdit {
    background: #1B243A;
    color: #FFFFFF;
    border: 2px solid #4C5BFF;
    border-radius: 10px;
    padding: 12px 15px;
    font-size: 14px;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QLineEdit:focus {
    border: 2px solid #6366F1;
    background: #1E2A40;
}

QLabel {
    color: #E2E8F0;
    font-size: 14px;
    font-weight: bold;
    padding: 5px;
}

QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #6366F1);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    padding: 12px 20px;
    min-width: 120px;
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #6366F1, stop: 1 #7C3AED);
}
"""

# Estilos para el historial
ESTILOS_HISTORIAL = """
QDialog {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #0B1D4A, stop: 1 #1F2A56);
}

#historialTitulo {
    color: #ffffff;
    font-size: 24px;
    font-weight: bold;
    padding: 20px;
}

#statsLabel {
    color: #94A3B8;
    font-size: 14px;
    padding: 10px 20px;
}

#listaSesiones {
    background: #141F3C;
    color: #ffffff;
    border: 2px solid #4C5BFF;
    border-radius: 15px;
    font-size: 14px;
    padding: 10px;
}

#listaSesiones::item {
    padding: 15px;
    border-bottom: 1px solid #4C5BFF;
    border-radius: 8px;
    margin: 3px;
}

#listaSesiones::item:selected {
    background: #4C5BFF;
}

#listaSesiones::item:hover {
    background: #1E3058;
}

#areaContenido {
    background: #141F3C;
    color: #ffffff;
    border: 2px solid #4C5BFF;
    border-radius: 15px;
    font-size: 14px;
    padding: 15px;
}

#botonHistorial {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #4C5BFF, stop: 1 #5A47F3);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    padding: 15px 25px;
    min-width: 140px;
}

#botonHistorial:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                              stop: 0 #6366F1, stop: 1 #7C3AED);
}
"""

# Función para obtener todos los estilos combinados
def obtener_estilos_completos():
    """Retorna todos los estilos CSS combinados"""
    return ESTILOS_ASISTENTE_PRINCIPAL

def obtener_estilos_panel_qa():
    """Retorna estilos específicos para el panel QA"""
    return ESTILOS_PANEL_QA

def obtener_estilos_configuracion():
    """Retorna estilos para diálogos de configuración"""
    return ESTILOS_CONFIGURACION

def obtener_estilos_historial():
    """Retorna estilos para el historial"""
    return ESTILOS_HISTORIAL
