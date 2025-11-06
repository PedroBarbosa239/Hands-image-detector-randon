# 🖐️ Detecção de Gestos com OpenCV e MediaPipe

Projeto tem como base estudo de visão computacional ultilizando a **MediaPipe**, ele tem tom humoristico e foi desenvolvido 
a partir de uma idéia do projeto da desenvolvedora Gabriela Marculino, onde seu [projeto](https://github.com/GabrielaMarculino/Nu-Metal-Pose-Random-Image-Detector) inspirou a confeccção do meu projeto

Este projeto utiliza **OpenCV**, **MediaPipe** e **NumPy** para detectar gestos com as mãos em tempo real via webcam.  
Cada gesto reconhecido exibe uma imagem correspondente a cada mão detectada, com efeito de transição suave (fade in/out).

---

## 🎯 Objetivo

Demonstrar o uso de visão computacional para:
- Rastrear mãos em tempo real;
- Identificar gestos específicos (ex: "Rock", "Joinha", "Dedo do meio", etc.);
- Exibir imagens personalizadas de acordo com o gesto reconhecido.

---

## 🧠 Tecnologias Utilizadas

- [OpenCV](https://opencv.org/) → Captura e manipulação de imagens/vídeo.  
- [MediaPipe](https://developers.google.com/mediapipe) → Detecção e rastreamento das mãos.  
- [NumPy](https://numpy.org/) → Processamento de arrays numéricos.  
- [Python 3.x](https://www.python.org/)  

---

## 📁 Estrutura do Projeto

> Dentro da pasta **img/** ficam as imagens correspondentes a cada gesto.  
> O nome das subpastas deve ser exatamente igual ao especificado no código:
> `"Nu_metal"`, `"Joinha"`, `"Rock"`, `"Dedo_do_meio"`.

---

## ⚙️ Instalação

1. **Clone este repositório**
   ```bash
   git clone https://github.com/PedroBarbosa239/Hands-image-detector-randon.git
   cd NOME_DO_REPOSITORIO
2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**
   ```bash
     python -m venv venv
    venv\Scripts\activate       # Windows
    source venv/bin/activate    # Linux / macOS
3. **Instale as dependências**
   ```bash
     pip install opencv-python mediapipe numpy
   
## 👨‍💻 Autor

Pedro Barbosa de Souza
- 📘 Projeto desenvolvido para estudo e prática de visão computacional em Python.
- 🔗 GitHub: Pedro Barbosa

## 📜 Licença

Este projeto é distribuído sob a licença MIT License.
Você pode usar, copiar, modificar e distribuir este projeto livremente para fins educacionais e experimentais.

## 📜💡 Sugestões Futuras
  Livres para contribuições no projeto e idéias e criticas 








