# 🤖 MAP - Detector de Fadiga (Protótipo IoT/IoB)

Disciplina: Physical Computing: IoT & IoB <br>
Grupo: G³ <br>
Turma: Engenharia de Software - 3º Ano

Integrantes: 
- Gilson Dias - RM552345
- Gustavo Bezerra - RM553076
- Gabriel de Mendonça - RM553149
- Larissa Estella - RM552695

<br>

## 💡 Problema e Solução Proposta

### O Problema
A Care Plus precisa de soluções digitais inovadoras para prevenção e bem-estar, sem recorrer a diagnósticos clínicos ou telemedicina, que são proibidos pelo desafio. O desafio é criar engajamento para hábitos saudáveis.

### A Solução: MAP 
A nossa ideia é desenvolver um novo módulo de gamificação para o aplicativo da Care Plus. O núcleo dessa plataforma será um "avatar", uma personificação digital do usuário. O objetivo é usar esse avatar para motivar o usuário a adotar uma postura proativa em relação à sua saúde. 

<br>

## 🎯 Objetivo do Projeto

O objetivo deste protótipo é desenvolver uma solução inovadora de saúde digital que promova o bem-estar e a prevenção, alinhada ao propósito da Care Plus.<br>

O módulo Detector de Fadiga utiliza Visão Computacional (IA/ML) para analisar o estado do usuário em tempo real, monitorando sinais de cansaço extremo (micro-sonos e bocejos). Ao detectar fadiga, o sistema gera um score que simula o dado que seria enviado à API do projeto (SOA), incentivando o usuário a registrar horas de sono no aplicativo "MAP" para recuperar a energia do seu avatar.

> ⚠️ **Nota de Conformidade:** Esta solução é um protótipo, **não realiza diagnóstico clínico** e **não se enquadra como telemedicina**.

<br>

## ✨ Funcionalidades

- Detecção de Micro-Sono (EAR): Analisa a Proporção da Abertura do Olho (EAR) para identificar piscadas longas (sinais de sonolência).<br>

- Detecção de Bocejo (MAR): Analisa a Proporção da Abertura da Boca (MAR) para identificar movimentos de bocejo.

- Gamificação Visual: Exibe uma Barra de Energia do Avatar que diminui com a fadiga e muda de cor (Verde -> Vermelho).

- Alerta Sonoro e Visual: Emite um alerta de alto contraste e sonoro quando o nível de fadiga atinge um ponto crítico.

- Log de Dados: Registra eventos de fadiga em um arquivo CSV (log_sessao_*.csv), simulando a telemetria do dispositivo IoT para o back-end (SOA).

- Display Técnico: Exibe a detecção em tela por meio de landmarks (pontos faciais) e valores de EAR/MAR, conforme exigido.

<br>

## ⚙️ Configuração e Execução

### Dependências

O projeto requer **Python 3.x** e as seguintes bibliotecas. Instale-as via `pip`:

```bash
pip install opencv-python mediapipe numpy
```

#### Nota: 'winsound' é nativo do Windows e usado para o alerta sonoro.

<br>

### Parâmetros Ajustáveis

Essas variáveis controlam a sensibilidade da detecção. 
| Variável no Código | Descrição | Valor Padrão |
| :--- | :---: | ---: |
| LIMIAR_EAR_FECHADO | Proporção abaixo da qual o olho é considerado fechado. | 0.23 | 
| LIMIAR_MAR_BOCEJO | Proporção que a boca deve atingir para ser contada como bocejo. | 0.90 | 
| FRAMES_PARA_MICRO_SONO | Número de frames que o olho deve estar fechado para pontuar. | 20 | 

<br>

### Instruções de Execução

Garanta que as dependências estejam instaladas.
Execute o script Python
O programa iniciará a câmera e a detecção.
Pressione a tecla q para encerrar. O log de eventos será salvo em um arquivo .csv na pasta.

<br>

### 🔒 Nota Ética sobre o Uso de Dados Faciais

O desenvolvimento desta solução seguiu rigorosos padrões de privacidade, conforme exigido
- Processamento Local (On-Device): A análise das imagens da webcam e dos marcos faciais (landmarks) é realizada localmente em tempo real no dispositivo do usuário.
- Não Armazenamento de Imagens: Nenhuma imagem, vídeo ou dado biométrico primário é armazenado, gravado ou transmitido para servidores remotos.
- Dados Coletados: Os únicos dados logados e salvos (no arquivo CSV) são métricas anônimas de eventos (Timestamp, Score de Fadiga, EAR, MAR).
- Conformidade: O protótipo está alinhado aos princípios da LGPD, pois armazena apenas dados de comportamento e não dados pessoais sensíveis que permitam a identificação do indivíduo.

