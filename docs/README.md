<h1>Xlerion - Video 2 Anim</h1>
<h3>Español (Spanish)</h3>
<p>Este proyecto es una aplicación de escritorio completa en Python que utiliza una interfaz gráfica para gestionar un pipeline de captura de movimiento, desde un video hasta un archivo de animación 3D (.bvh).</p>

Webpage:
<link>https://mikehell84.github.io/Xlerion-Video-2-Anim/</link>

<img width="1460" height="847" alt="image" src="https://github.com/user-attachments/assets/aed68fc4-3736-43c7-813f-d38d12e82aae" />


<h3>Características Principales</h1>
Interfaz Gráfica Intuitiva: Gestiona todo el proceso con botones y menús, sin necesidad de usar la línea de comandos.

<h4>Múltiples Modos de Captura:</h4>

Pose Corporal: Captura el esqueleto completo de una persona.

Manos (Alta Precisión): Se especializa en el movimiento detallado de los dedos.

Rostro y Gestos: Captura una malla facial de 478 puntos para expresiones.

Captura Flexible: Usa videos pregrabados o captura en tiempo real desde tu webcam con un temporizador.

Gestión de Sesiones: Guarda, carga y gestiona todas tus capturas en un panel dedicado.

Ajustes en Tiempo Real: Modifica los parámetros de detección para mejorar la calidad de la captura según tus necesidades.

Exportación a BVH: Convierte los datos de pose corporal a formato .bvh, compatible con la mayoría de software 3D.

Soporte Multilenguaje y Temas: Interfaz traducida a Español, Inglés y Japonés, con modo claro y oscuro.

<h2>1. Guía de Instalación (Entorno Controlado con Conda)</h2>
Para evitar problemas de compatibilidad, es altamente recomendable usar el gestor de entornos Conda.

<h3>1.1. Instalar Miniconda</h3>
Si no lo tienes, descarga e instala Miniconda.

Enlace de descarga: Miniconda para Windows

<h3>1.2. Crear y Activar el Entorno</h3>
Abre la Anaconda Prompt (miniconda3) desde tu menú de inicio.

Crea un nuevo entorno llamado mocap_env con Python 3.10:

*conda create --name mocap_env python=3.10*

Activa el entorno. Deberás hacer esto cada vez que abras una nueva terminal para trabajar en el proyecto:

*conda activate mocap_env*

<h3>1.3. Instalar Dependencias</h3>
Con el entorno (mocap_env) activado, instala todas las librerías necesarias con un solo comando:

pip install opencv-python pyyaml mediapipe numpy scipy Pillow

<h3>2. Cómo Ejecutar la Aplicación (Método Fácil)</h3>
Una vez instalado todo, puedes iniciar la aplicación fácilmente con un solo clic.

Usando el Lanzador start.cmd
Busca el archivo start.cmd en la carpeta principal del proyecto.

Haz doble clic en start.cmd.

Se abrirá una terminal que activará automáticamente el entorno y lanzará la aplicación gráfica. ¡No necesitas hacer nada más!

<h3>3. Cómo Usar la Interfaz</h3>
Panel de Sesiones (Izquierda): Aquí verás todas tus capturas guardadas. Puedes seleccionarlas para recargar sus datos, abrir su carpeta o eliminarlas.

<h4>Etapa 1: Captura de Datos:</h4>

Elige un Modo: En "Ajustes de Detección", selecciona si quieres capturar "Pose Corporal", "Manos" o "Rostro".

Selecciona una Fuente: Haz clic en "Seleccionar Video" para usar un archivo existente o en "Capturar desde Webcam" para una grabación en tiempo real.

Inicia la Captura: Presiona "Iniciar Captura". Al finalizar, la sesión se guardará automáticamente.

<h4>Etapa 2: Exportar Animación:</h4>

Selecciona una sesión de la lista que contenga datos de Pose Corporal.

Haz clic en "Exportar Animación". Se abrirá una ventana para que elijas el formato y guardes tu archivo .bvh.

Nota: La exportación a .bvh solo es compatible con los datos de "Pose Corporal".

<h3>4. Uso en Software 3D</h3>
El archivo .bvh generado se puede importar directamente en Blender, Unity, 3ds Max y otro software de animación 3D para aplicarlo a tus personajes.

*5. Licencia y Derechos de Autor*
Licencia del Proyecto
Este proyecto se distribuye bajo la Licencia MIT.

**Copyright (c) 2025 Miguel Rodriguez Martinez**

Por la presente se concede permiso, libre de cargos, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados (el "Software"), para comerciar con el Software sin restricción, incluyendo sin limitación los derechos de uso, copia, modificación, fusión, publicación, distribución, sublicencia, y/o venta de copias del Software, y para permitir a las personas a las que se les proporcione el Software que lo hagan, con sujeción a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas las copias o partes sustanciales del Software.

*EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIABILIDAD, IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN, DAÑO U OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O CUALQUIER OTRO MOTIVO, DERIVADA DE, FUERA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U OTROS TRATOS EN EL SOFTWARE.*

Reconocimientos y Colaboración
Este software utiliza librerías de terceros, incluyendo MediaPipe de Google (Licencia Apache 2.0) y OpenCV (Licencia Apache 2.0). Todos los derechos pertenecen a sus respectivos dueños.

El desarrollo del código fuente de esta aplicación fue realizado en colaboración con la IA de Google.

English (Inglés)
Xlerion - Video 2 Anim
This project is a complete desktop application in Python that uses a graphical interface to manage a motion capture pipeline, from a video to a 3D animation file (.bvh).

<h3>Key Features</h3>
Intuitive Graphical Interface: Manage the entire process with buttons and menus, without needing to use the command line.

<h4>Multiple Capture Modes:</h4>

**Body Pose: Captures a person's full skeleton.**

**Hands (High Precision): Specializes in detailed finger movement.**

**Face & Gestures: Captures a 478-point facial mesh for expressions.**

**Flexible Capture: Use pre-recorded videos or capture in real-time from your webcam with a timer.**

**Session Management: Save, load, and manage all your captures in a dedicated panel.**

**Real-Time Adjustments: Modify detection parameters to improve capture quality according to your needs.**

**Export to BVH: Convert body pose data to .bvh format, compatible with most 3D software.**

**Multi-language and Theme Support: Interface translated into Spanish, English, and Japanese, with light and dark modes.**

<h3>1. Installation Guide (Controlled Environment with Conda)</h3>
**To avoid compatibility issues, it is highly recommended to use the Conda environment manager.**

1.1. Install Miniconda
<h4>If you don't have it, download and install Miniconda.</h4>

Download link: Miniconda for Windows

<h2>1.2. Create and Activate the Environment</h2>
*Open the Anaconda Prompt (miniconda3) from your Start Menu.*

Create a new environment named mocap_env with Python 3.10:

conda create --name mocap_env python=3.10

Activate the environment. You will need to do this every time you open a new terminal to work on the project:

conda activate mocap_env

1.3. Install Dependencies
With the (mocap_env) environment activated, install all necessary libraries with a single command:

pip install opencv-python pyyaml mediapipe numpy scipy Pillow

2. How to Run the Application (Easy Method)
Once everything is installed, you can easily start the application with a single click.

Using the start.cmd Launcher
Find the start.cmd file in the main project folder.

Double-click on start.cmd.

A terminal will open, automatically activate the environment, and launch the graphical application. You don't need to do anything else!

3. How to Use the Interface
Sessions Panel (Left): Here you will see all your saved captures. You can select them to reload their data, open their folder, or delete them.

Stage 1: Data Capture:

Choose a Mode: In "Detection Settings", select whether you want to capture "Body Pose", "Hands", or "Face".

Select a Source: Click "Select Video" to use an existing file or "Capture from Webcam" for real-time recording.

Start Capture: Press "Start Capture". When finished, the session will be saved automatically.

<h2>Stage 2: Export Animation:</h2>

Select a session from the list that contains Body Pose data.

**Click "Export Animation". A window will open for you to choose the format and save your .bvh file.**

Note: Exporting to .bvh is only compatible with "Body Pose" data.

4. Usage in 3D Software
The generated .bvh file can be directly imported into Blender, Unity, 3ds Max, and other 3D animation software to apply to your characters.

5. License and Copyright
Project License
This project is distributed under the MIT License.

Copyright (c) 2025 Miguel Rodriguez Martinez

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Acknowledgments and Collaboration
This software uses third-party libraries, including MediaPipe by Google (Apache 2.0 License) and OpenCV (Apache 2.0 License). All rights belong to their respective owners.

The source code development of this application was carried out in collaboration with Google's AI.

日本語 (Japanese)
Xlerion - ビデオからアニメへ
このプロジェクトは、ビデオから3Dアニメーションファイル（.bvh）まで、モーションキャプチャパイプラインを管理するためのグラフィカルインターフェースを使用した、Pythonの完全なデスクトップアプリケーションです。

✨ 主な機能
直感的なグラフィカルインターフェース: コマンドラインを使用せずに、ボタンとメニューで全プロセスを管理。

複数のキャプチャモード:

全身ポーズ: 人物の完全なスケルトンをキャプチャ。

手（高精度）: 指の詳細な動きに特化。

顔とジェスチャー: 478点の顔メッシュをキャプチャして表情を表現。

柔軟なキャプチャ: 録画済みビデオを使用するか、タイマー付きのウェブカメラからリアルタイムでキャプチャ。

セッション管理: 専用パネルですべてのキャプチャを保存、読み込み、管理。

リアルタイム調整: ニーズに応じて検出パラメータを変更し、キャプチャ品質を向上。

BVHへのエクスポート: ほとんどの3Dソフトウェアと互換性のある.bvh形式に全身ポーズデータを変換。

多言語およびテーマのサポート: スペイン語、英語、日本語に翻訳されたインターフェース、ライトモードとダークモード付き。

1. インストールガイド（Condaによる管理環境）
互換性の問題を避けるため、Conda環境マネージャーの使用を強く推奨します。

1.1. Minicondaのインストール
まだインストールしていない場合は、Minicondaをダウンロードしてインストールしてください。

ダウンロードリンク: Miniconda for Windows

1.2. 環境の作成と有効化
スタートメニューから**Anaconda Prompt (miniconda3)**を開きます。

Python 3.10でmocap_envという名前の新しい環境を作成します:

conda create --name mocap_env python=3.10

環境を有効化します。プロジェクトで作業するために新しいターミナルを開くたびにこれを行う必要があります:

conda activate mocap_env

1.3. 依存関係のインストール
(mocap_env)環境を有効にした状態で、1つのコマンドで必要なすべてのライブラリをインストールします:

pip install opencv-python pyyaml mediapipe numpy scipy Pillow

2. アプリケーションの実行方法（簡単な方法）
すべてインストールしたら、ワンクリックで簡単にアプリケーションを起動できます。

start.cmdランチャーの使用
メインプロジェクトフォルダでstart.cmdファイルを見つけます。

start.cmdをダブルクリックします。

ターミナルが開き、自動的に環境を有効化してグラフィカルアプリケーションを起動します。これ以上何もする必要はありません！

3. インターフェースの使用方法
セッションパネル（左側）: 保存したすべてのキャプチャが表示されます。選択してデータを再読み込みしたり、フォルダを開いたり、削除したりできます。

ステージ1: データキャプチャ:

モードを選択: 「検出設定」で、「全身ポーズ」、「手」、または「顔」をキャプチャするかどうかを選択します。

ソースを選択: 「ビデオを選択」をクリックして既存のファイルを使用するか、「ウェブカメラからキャプチャ」をクリックしてリアルタイムで録画します。

キャプチャを開始: 「キャプチャ開始」を押します。終了すると、セッションは自動的に保存されます。

ステージ2: アニメーションのエクスポート:

全身ポーズデータを含むセッションをリストから選択します。

「アニメーションをエクスポート」をクリックします。ウィンドウが開き、フォーマットを選択して.bvhファイルを保存できます。

注意: .bvhへのエクスポートは「全身ポーズ」データとのみ互換性があります。

4. 3Dソフトウェアでの使用
生成された.bvhファイルは、Blender、Unity、3ds Maxなどの3Dアニメーションソフトウェアに直接インポートして、キャラクターに適用できます。

5. ライセンスと著作権
プロジェクトライセンス
このプロジェクトはMITライセンスの下で配布されています。

Copyright (c) 2025 Miguel Rodriguez Martinez

これにより、本ソフトウェアおよび関連ドキュメントファイル（以下「本ソフトウェア」）のコピーを取得するすべての人に対し、使用、コピー、変更、マージ、公開、配布、サブライセンス、および/または本ソフトウェアのコピーの販売、ならびに本ソフトウェアが提供される人にそれを許可する権利を含むがこれに限定されない、制限なしに本ソフトウェアを扱うための許可を無償で付与します。ただし、以下の条件に従うものとします。

上記の著作権表示およびこの許可表示は、本ソフトウェアのすべてのコピーまたは実質的な部分に含まれるものとします。

本ソフトウェアは「現状有姿」で提供され、商品性、特定目的への適合性、および非侵害の保証を含むがこれに限定されない、明示または黙示を問わず、いかなる種類の保証もありません。いかなる場合も、作者または著作権者は、契約行為、不法行為、またはその他の理由であるかを問わず、本ソフトウェアまたはその使用またはその他の取引に起因または関連して生じるいかなる請求、損害、またはその他の責任も負わないものとします。

謝辞と協力
このソフトウェアは、GoogleのMediaPipe（Apache 2.0ライセンス）やOpenCV（Apache 2.0ライセンス）を含むサードパーティのライブラリを使用しています。すべての権利はそれぞれの所有者に帰属します。

このアプリケーションのソースコード開発は、GoogleのAIとの協力のもとで行われました。
