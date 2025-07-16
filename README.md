# Euler App — Visualização da Fórmula de Euler

Este é um aplicativo interativo feito com [Streamlit](https://streamlit.io) para visualizar a fórmula de Euler:

\[
e^{ix} = \cos(x) + i\sin(x)
\]

## 🚀 Funcionalidades

- Gráfico do círculo unitário no plano complexo
- Vetores interativos de \cos(x), \sin(x) e \(e^{ix}\)
- Áudio narrado com explicação da fórmula
- Exportar gráfico como PNG
- Gerar PDF com explicação + gráfico

## 📁 Estrutura

```
euler_app/
├── app.py
├── requirements.txt
├── README.md
└── assets/
    └── explicacao_euler.mp3
```

## ▶️ Como executar

1. Instale os requisitos:

```
pip install -r requirements.txt
```

2. Execute o aplicativo:

```
streamlit run app.py
```

---