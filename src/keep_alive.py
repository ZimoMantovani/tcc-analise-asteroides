"""
Abre o app Streamlit (neo-analyser), acorda ele se estiver hibernando
e clica no botão "INICIAR VARREDURA (ATUALIZAR)" para:
  1) contar como uso real da sessão (evita a hibernação do Streamlit Cloud)
  2) disparar o ETL normal, que já atualiza sozinho o carimbo
     "ATUALIZADO ..." mostrado na sidebar (lido do banco a cada load)

Roda via .github/workflows/keep-alive.yml
"""

import os
import sys

from playwright.sync_api import sync_playwright

APP_URL = os.environ.get("APP_URL", "https://neo-analyser.streamlit.app/")
WAKE_BUTTON = "Yes, get this app back up!"
SCAN_BUTTON = "INICIAR VARREDURA (ATUALIZAR)"
COLD_START_TIMEOUT_MS = 5 * 60 * 1000  # cold start do Streamlit Cloud pode levar minutos
SCAN_TIMEOUT_MS = 90 * 1000


def log(msg: str) -> None:
    print(f"[keep-alive] {msg}", flush=True)


def fail(page, motivo: str, arquivo: str) -> None:
    page.screenshot(path=arquivo)
    log(f"ERRO: {motivo} (screenshot salvo em {arquivo})")
    sys.exit(1)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        log(f"Abrindo {APP_URL}")
        page.goto(APP_URL, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(4000)

        wake_btn = page.get_by_role("button", name=WAKE_BUTTON)
        if wake_btn.count() > 0:
            log("App estava dormindo. Clicando para acordar...")
            wake_btn.click()
            try:
                page.get_by_role("button", name=SCAN_BUTTON).wait_for(
                    state="visible", timeout=COLD_START_TIMEOUT_MS
                )
                log("App acordou e a página carregou.")
            except Exception:
                fail(page, "o app não terminou de acordar a tempo", "falha_wakeup.png")
        else:
            log("App já estava acordado.")

        scan_btn = page.get_by_role("button", name=SCAN_BUTTON)
        try:
            scan_btn.wait_for(state="visible", timeout=30_000)
        except Exception:
            fail(page, "não encontrei o botão de varredura na página", "falha_botao_nao_encontrado.png")

        scan_btn.click()
        log("Cliquei em 'INICIAR VARREDURA (ATUALIZAR)', aguardando conclusão...")

        # Espera o spinner "Extraindo telemetria da NASA..." sumir, se der tempo de pegar
        try:
            page.get_by_text("Extraindo telemetria da NASA").wait_for(
                state="hidden", timeout=SCAN_TIMEOUT_MS
            )
        except Exception:
            pass  # spinner pode já ter sumido rápido demais pra capturar, sem problema

        page.wait_for_timeout(3000)
        page.screenshot(path="resultado_varredura.png")
        log("Concluído. Screenshot final salvo em resultado_varredura.png")
        browser.close()


if __name__ == "__main__":
    main()
