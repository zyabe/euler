import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import tempfile
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

# Configura página
st.set_page_config(layout="wide", page_title="Visualização de Euler")
st.title("🌀 Visualização de $e^{ix} = \cos(x) + i\\sin(x)$")

# 🔊 Áudio explicativo
with st.expander("🔊 Ouça a explicação da fórmula de Euler"):
    st.audio("assets/explicacao_euler.mp3")

# 🎛️ Slider interativo
x = st.slider("Escolha o valor de x (em radianos):", 0.0, 2*np.pi, 0.0, step=0.01)
z = np.exp(1j * x)
cosx = np.cos(x)
sinx = np.sin(x)

# 🎨 Gerar gráfico
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_title("Plano complexo")

# Círculo unitário
circle = plt.Circle((0, 0), 1, fill=False, linestyle="--", color="gray")
ax.add_artist(circle)

# Vetores
ax.plot([0, z.real], [0, z.imag], 'r-', lw=2, label=r"$e^{ix}$")
ax.plot(z.real, z.imag, 'ro')
ax.plot([0, cosx], [0, 0], 'b--', label=r"$\cos(x)$")
ax.plot([cosx, cosx], [0, sinx], 'g--', label=r"$\sin(x)$")
ax.plot(cosx, 0, 'bo')
ax.plot(cosx, sinx, 'go')

ax.legend(loc='upper left')
ax.grid(True)
ax.set_xlabel("Re (Real)")
ax.set_ylabel("Im (Imaginário)")
st.pyplot(fig)

# 📥 Download da imagem PNG
buf = io.BytesIO()
fig.savefig(buf, format="png")
st.download_button("📷 Baixar gráfico como imagem", data=buf.getvalue(),
                   file_name="grafico_euler.png", mime="image/png")

# 📊 Mostrar valores
st.markdown(f"""
### 📊 Valores numéricos:
- \( x = {x:.3f} \) rad
- \( \cos(x) = {cosx:.3f} \)
- \( \sin(x) = {sinx:.3f} \)
- \( e^{{ix}} = {z.real:.3f} + {z.imag:.3f}i \)
""")

# 📄 Gerar PDF com gráfico e explicação
def gerar_pdf(x, cosx, sinx, z, fig):
    buffer_pdf = io.BytesIO()
    c = canvas.Canvas(buffer_pdf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height - 2*cm, "Visualização da Fórmula de Euler")

    texto = (
        f"A fórmula de Euler conecta a função exponencial complexa com trigonometria:\n"
        f"    e^ix = cos(x) + i·sin(x)\n\n"
        f"Para x = {x:.3f} rad:\n"
        f" - cos(x) = {cosx:.3f}\n"
        f" - sin(x) = {sinx:.3f}\n"
        f" - e^ix = {z.real:.3f} + {z.imag:.3f}i\n\n"
        f"O gráfico abaixo mostra a posição de e^ix no círculo unitário."
    )

    c.setFont("Helvetica", 12)
    text_obj = c.beginText(2*cm, height - 3.5*cm)
    for linha in texto.split('\n'):
        text_obj.textLine(linha)
    c.drawText(text_obj)

    # Salvar imagem temporária
    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.savefig(temp_img.name, format="png", bbox_inches="tight")
    temp_img.close()

    # Adicionar imagem ao PDF
    img = Image.open(temp_img.name)
    img_width, img_height = img.size
    aspect = img_height / img_width
    target_width = width - 4*cm
    target_height = target_width * aspect

    c.drawImage(ImageReader(temp_img.name), 2*cm, height - 3.5*cm - target_height - 1*cm,
                width=target_width, height=target_height)

    c.showPage()
    c.save()
    buffer_pdf.seek(0)
    return buffer_pdf

# Botão para download do PDF
pdf_bytes = gerar_pdf(x, cosx, sinx, z, fig)
st.download_button("📄 Baixar PDF com gráfico e explicação",
                   data=pdf_bytes,
                   file_name="formula_euler.pdf",
                   mime="application/pdf")
