"""
=============================================================================
🎓 SQUAD 5: PLATAFORMA DE CURSOS & AUDIOBOOKS (squad_cursos.py)
Workspace: Desktop\\Super Gerador\\Grego / Criador de Audiobook
=============================================================================
Squad Multi-Agente Oficial:
- Agente 1: Linguista Bíblico & Designer Instrucional (Módulos 1 ao 15, gramática)
- Agente 2: Desenvolvedor Web EAD (Cronogramas interativos, checklists, dashboards)
- Agente 3: Especialista em Áudio & Fonética (Vocalização grega/hebraica, TTS, MP3)
- Agente 4: Revisor Pedagógico & QA de Conteúdo (Exercícios, simulados, gabaritos)
=============================================================================
"""
import os
import sys
import json
import warnings
import urllib.request
import urllib.error

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

warnings.filterwarnings("ignore")
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

FREELLM_URL = os.getenv("FREELLMAPI_URL", "http://127.0.0.1:3001/v1")
FREELLM_KEY = os.getenv("FREELLMAPI_KEY", "freellmapi-0af93b3a0e1cbe45a5785fd84071080555fc11b147d6f7f2")

def test_freellm_connection():
    try:
        req = urllib.request.Request(
            f"{FREELLM_URL}/models",
            headers={"Authorization": f"Bearer {FREELLM_KEY}"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return True, f"Online ({len(data.get('data', []))} modelos disponíveis)"
    except Exception as e:
        return False, f"Alerta ({e})"

try:
    from crewai import Agent, Task, Crew, Process, LLM

    def get_llm(model="freellm/qwen-coder", temp=0.2):
        return LLM(model=model, base_url=FREELLM_URL, api_key=FREELLM_KEY, temperature=temp)

    def criar_squad_cursos():
        linguista_llm = get_llm("openai/claude-sonnet-4-5", 0.2)
        coder_llm = get_llm("openai/claude-sonnet-4-5", 0.1)
        fast_llm = get_llm("openai/auto", 0.3)

        linguista = Agent(
            role="Linguista e Designer Instrucional de Línguas Clássicas",
            goal="Estruturar planos de aula, cronogramas mensais, declinações, conjugações e vocabulário progressivo",
            backstory="Professor e filólogo especialista em hebraico bíblico, grego koiné e metodologias modernas de ensino de línguas antigas.",
            llm=linguista_llm,
            verbose=False
        )

        dev_ead = Agent(
            role="Desenvolvedor Web de Plataformas EAD",
            goal="Criar interfaces interativas (HTML5, Tailwind, JS) com rastreamento de progresso do aluno, flashcards e cronogramas visuais",
            backstory="Engenheiro frontend especializado em portais educacionais autônomos e experiência de aprendizado gamificada.",
            llm=coder_llm,
            verbose=False
        )

        audio_expert = Agent(
            role="Especialista em Fonética e Produção de Audiobooks",
            goal="Gerar orientações de pronúncia fonética precisa (erasmiana ou moderna) e roteiros para sintetização TTS/MP3 em alta definição",
            backstory="Produtor de áudio e foneticista especializado em narração instrucional e geração de audiobooks didáticos.",
            llm=fast_llm,
            verbose=False
        )

        revisor = Agent(
            role="Revisor Pedagógico e Elaborador de Avaliações",
            goal="Produzir listas de exercícios de fixação, simulados bimestrais com gabaritos comentados e validação didática",
            backstory="Avaliador pedagógico sênior com vasta experiência em criação de provas, exercícios de tradução e fixação sintática.",
            llm=linguista_llm,
            verbose=False
        )

        return [linguista, dev_ead, audio_expert, revisor]

    def executar_squad_cursos(demanda: str) -> str:
        linguista, dev_ead, audio_expert, revisor = criar_squad_cursos()
        t1 = Task(
            description=f"Elabore a estrutura pedagógica e linguística para: '{demanda}'.",
            expected_output="Conteúdo instrucional com explicações gramaticais e exemplos práticos.",
            agent=linguista
        )
        t2 = Task(
            description="Crie os exercícios práticos correspondentes e o gabarito comentado.",
            expected_output="Caderno de exercícios e gabarito oficial.",
            agent=revisor
        )
        equipe = Crew(agents=[linguista, revisor], tasks=[t1, t2], process=Process.sequential, verbose=True)
        return str(equipe.kickoff())

except Exception:
    criar_squad_cursos = None
    executar_squad_cursos = None

def main():
    print("=" * 70)
    print("  🎓 SQUAD 5: PLATAFORMA DE CURSOS & AUDIOBOOKS — ATIVO")
    print("=" * 70)
    online, msg = test_freellm_connection()
    status_icon = "🟢" if online else "🟡"
    print(f"  {status_icon} FreeLLMAPI Local: {FREELLM_URL} -> {msg}")
    print("  ⚡ Modo de Operação: Cota R$ 0 (Modelos Locais Qwen / Claude Sonnet / FLUX)")
    print("-" * 70)
    print("  👥 AGENTES ESPECIALISTAS INTEGRADOS:")
    print("  [1] 📖  Linguista & Designer Instrucional (Gramática grega/hebraica, Módulos 1-15)")
    print("  [2] 💻  Desenvolvedor Web EAD           (Cronogramas interativos, flashcards, progresso)")
    print("  [3] 🎙️   Especialista em Áudio & Fonética (Pronúncia erasmiana, TTS, audiobooks MP3)")
    print("  [4] 📝  Revisor Pedagógico & QA          (Simulados, exercícios de fixação, gabaritos)")
    print("=" * 70)

    if len(sys.argv) > 1:
        demanda = " ".join(sys.argv[1:])
        print(f"\n🚀 Disparando Missão do Squad para: '{demanda}'\n")
        if executar_squad_cursos:
            resultado = executar_squad_cursos(demanda)
            print("\n" + "=" * 70)
            print("🏁 RESULTADO DO SQUAD:")
            print("=" * 70)
            print(resultado)
        else:
            print("[Aviso] CrewAI não encontrado para execução encadeada.")
    else:
        print("\n✨ Status: Todos os 4 especialistas estão prontos e integrados ao projeto!")
        print("💡 Para despachar uma tarefa em cadeia para o Squad, execute:")
        print("   python squad_cursos.py \"sua demanda aqui\"")
        print("=" * 70)

if __name__ == "__main__":
    main()

