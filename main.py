# -*- coding: utf-8 -*-
import kivy
import math
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
import logging
logging.basicConfig(level=logging.DEBUG)

kivy.logger.Logger.setLevel("DEBUG")

class ButtonCustom(ButtonBehavior, BoxLayout):
    img_source = StringProperty('')
    text_label = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 2
        self.size_hint = (None, None)
        self.size = (180, 90)
        self.padding = [5, 5]

def toggle_menu(self):
    if self.ids.menu.pos_hint["x"] == -1:
        self.ids.menu.pos_hint = {"x": 0}
    else:
        self.ids.menu.pos_hint = {"x": -1}

Factory.register('ButtonCustom', cls=ButtonCustom)  # Registra a classe no Factory

class ExplanatoryBox(FloatLayout):
    explanation_title = StringProperty('')
    explanation_text_before_image = StringProperty('')
    explanation_text_between_images = StringProperty('')
    explanation_text_after_images = StringProperty('')
    explanation_image_path = StringProperty('')
    additional_image_path = StringProperty('')

class ButtonCustomCalculadora(ButtonBehavior, BoxLayout):
    img_source = StringProperty('')
    text_label = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 2
        self.size_hint = (None, None)
        self.size = (180, 120)  # Ajuste o tamanho conforme necessário
        self.padding = [5, 5]

    # registra a classe para ser usada no arquivo .kv
Factory.register('ButtonCustomCalculadora', cls=ButtonCustomCalculadora)
GUI = Builder.load_file("estrutura.kv")

class ButtonSimbologia(Button):
    img_source = StringProperty("")
    text_label = StringProperty("")
    explanation_text = StringProperty("")

    def on_release(self):
        box = ModalView(size_hint=(1, 1), auto_dismiss=True)
        content = ExplanatoryBox(
            explanation_title=self.text_label,
            explanation_text=self.explanation_text
        )
        box.add_widget(content)
        box.open()

Factory.register('ButtonSimbologia', cls=ButtonSimbologia)  # Registra a classe no Factory

class ImageButton(ButtonBehavior, Image):
    pass

class GerenciadorTelas(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TelaInicial(Screen):
    pass

class CalculosdeSoldagem(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False

    def on_pre_enter(self, *args):
        # Chamado sempre que a tela está prestes a ser exibida
        Logger.info("CalculosdeSoldagem: on_pre_enter")
        self.menu_aberto = False
        menu_layout = self.ids.menu_layout

        # Cancela animações pendentes e redefine o estado inicial do menu
        Animation.cancel_all(menu_layout)
        menu_layout.opacity = 0
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        # Posição inicial fora da tela (à direita, alinhado ao TOPO)
        menu_layout.pos = (Window.width, target_y_top)

        menu_layout.disabled = True
        Logger.info(f"CalculosdeSoldagem: on_pre_enter - Initial menu pos set to: {menu_layout.pos}")

    def _on_menu_close_complete(self, animation, widget):
        Logger.info(f"CalculosdeSoldagem: Menu close animation complete. Disabling widget: {widget}")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        """Chamado quando a animação de abrir o menu termina."""
        Logger.info(f"CalculosdeSoldagem: Menu open animation complete for widget: {widget}")

    def open_menu(self):
        menu_layout = self.ids.menu_layout

        Logger.info(f"CalculosdeSoldagem: open_menu called. Current menu_aberto: {self.menu_aberto}")
        Logger.info(
            f"CalculosdeSoldagem: menu_layout initial - pos: {menu_layout.pos}, size: {menu_layout.size}, opacity: {menu_layout.opacity}, disabled: {menu_layout.disabled}")
        Logger.info(f"CalculosdeSoldagem: Window.width: {Window.width}, menu_layout.width: {menu_layout.width}, Window.height: {Window.height}, menu_layout.height: {menu_layout.height}")

        Animation.cancel_all(menu_layout)

        # A largura do menu deve ser (size_hint_x * parent.width).
        current_menu_width = menu_layout.width
        if current_menu_width == 0 and menu_layout.size_hint_x is not None and menu_layout.parent:
            calculated_width = menu_layout.size_hint_x * menu_layout.parent.width
            Logger.warning(
                f"CalculosdeSoldagem: menu_layout.width is 0! Using calculated width based on size_hint: {calculated_width}. This might indicate a timing issue.")
            # If width is 0, the X calculation will be wrong, but let's proceed for the Y part.

        # Posição X para o menu aberto (borda esquerda do menu)
        target_x_open = Window.width - current_menu_width
        # Posição X para o menu fechado (borda esquerda do menu fora da tela à direita)
        off_screen_x = Window.width

        # --- MODIFICAÇÃO PARA MANTER A POSIÇÃO Y NO TOPO DURANTE A ANIMAÇÃO ---
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        Logger.info(f"CalculosdeSoldagem: open_menu - menu_layout.height: {menu_layout.height}, Window.height: {Window.height}, target_y_top: {target_y_top}")
        # --- FIM DA MODIFICAÇÃO ---

        Logger.info(
            f"CalculosdeSoldagem: Calculated animation positions - target_x_open: {target_x_open}, off_screen_x: {off_screen_x}, target_y_top: {target_y_top}")

        if self.menu_aberto:  # Se o menu está aberto, vamos fechá-lo
            Logger.info("CalculosdeSoldagem: Closing menu...")
            # --- MODIFICAÇÃO NA ANIMAÇÃO DE FECHAR ---
            anim = Animation(pos=(off_screen_x, target_y_top), opacity=0, duration=0.2)
            # --- FIM DA MODIFICAÇÃO ---
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False  # Atualiza o estado
        else:  # Se o menu está fechado, vamos abri-lo
            Logger.info("CalculosdeSoldagem: Opening menu...")
            menu_layout.disabled = False  # Habilita antes da animação
            # --- MODIFICAÇÃO NA ANIMAÇÃO DE ABRIR ---
            anim = Animation(pos=(target_x_open, target_y_top), opacity=1, duration=0.2)
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True  # Atualiza o estado

        anim.start(menu_layout)
        Logger.info(
            f"CalculosdeSoldagem: Animation started. New menu_aberto: {self.menu_aberto}. Target widget: {menu_layout}")

    def on_touch_down(self, touch):
        menu_layout = self.ids.menu_layout

        # Verifica se o menu está aberto e se o clique ocorreu fora do menu
        if self.menu_aberto and menu_layout.opacity > 0:
            if not menu_layout.collide_point(*touch.pos):
                Logger.info("CalculosdeSoldagem: Touch outside open menu detected. Closing menu.")
                self.open_menu()  # Fecha o menu
                return True  # Consome o evento de toque para evitar que outros widgets reajam
            else:
                # Clique dentro do menu, permite que os botões funcionem
                return super().on_touch_down(touch)

        # Permite que o clique em outros widgets funcione normalmente
        return super().on_touch_down(touch)

class Calculo1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False
        self.explanatory_box = None  # Armazena a referência da caixa explicativa

    def on_pre_enter(self, *args):
        Logger.info("Calculo1: on_pre_enter")
        self.menu_aberto = False
        menu_layout = self.ids.menu_layout

        # Cancela animações pendentes e redefine o estado inicial do menu
        Animation.cancel_all(menu_layout)
        menu_layout.opacity = 0
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        # Posição inicial fora da tela (à direita, alinhado ao TOPO)
        menu_layout.pos = (Window.width, target_y_top)

        menu_layout.disabled = True
        Logger.info(f"Calculo1: on_pre_enter - Initial menu pos set to: {menu_layout.pos}")

        # Fecha a caixa explicativa, se estiver aberta
        self.close_explanatory_box()

        # Limpa os campos de entrada
        self.ids.input_1.text = ""
        self.ids.input_2.text = ""
        self.ids.input_3.text = ""
        self.ids.input_4.text = ""

    def _on_menu_close_complete(self, animation, widget):
        """Chamado quando a animação de fechar o menu termina."""
        Logger.info(f"Calculo1: Menu close animation complete. Disabling widget: {widget}")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        """Chamado quando a animação de abrir o menu termina."""
        Logger.info(f"Calculo1: Menu open animation complete for widget: {widget}")
        # Nenhuma ação específica aqui por enquanto

    def open_menu(self):
        menu_layout = self.ids.menu_layout

        Logger.info(f"Calculo1: open_menu called. Current menu_aberto: {self.menu_aberto}")
        Logger.info(
            f"Calculo1: menu_layout initial - pos: {menu_layout.pos}, size: {menu_layout.size}, opacity: {menu_layout.opacity}, disabled: {menu_layout.disabled}")
        Logger.info(f"Calculo1: Window.width: {Window.width}, menu_layout.width: {menu_layout.width}, Window.height: {Window.height}, menu_layout.height: {menu_layout.height}")

        # Cancela qualquer animação em progresso no menu_layout
        Animation.cancel_all(menu_layout)

        current_menu_width = menu_layout.width
        if current_menu_width == 0 and menu_layout.size_hint_x is not None and menu_layout.parent:
            calculated_width = menu_layout.size_hint_x * menu_layout.parent.width
            Logger.warning(
                f"Calculo1: menu_layout.width is 0! Using calculated width based on size_hint: {calculated_width}. This might indicate a timing issue.")

        # Posição X para o menu aberto (borda esquerda do menu)
        target_x_open = Window.width - current_menu_width
        # Posição X para o menu fechado (borda esquerda do menu fora da tela à direita)
        off_screen_x = Window.width

        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        Logger.info(f"Calculo1: open_menu - menu_layout.height: {menu_layout.height}, Window.height: {Window.height}, target_y_top: {target_y_top}")

        Logger.info(
            f"Calculo1: Calculated animation positions - target_x_open: {target_x_open}, off_screen_x: {off_screen_x}, target_y_top: {target_y_top}")

        if self.menu_aberto:  # Se o menu está aberto, vamos fechá-lo
            Logger.info("Calculo1: Closing menu...")
            anim = Animation(pos=(off_screen_x, target_y_top), opacity=0, duration=0.2)
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False  # Atualiza o estado
        else:  # Se o menu está fechado, vamos abri-lo
            Logger.info("Calculo1: Opening menu...")
            menu_layout.disabled = False  # Habilita antes da animação
            anim = Animation(pos=(target_x_open, target_y_top), opacity=1, duration=0.2)
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True

        anim.start(menu_layout)
        Logger.info(
            f"Calculo1: Animation started. New menu_aberto: {self.menu_aberto}. Target widget: {menu_layout}")

    def on_touch_down(self, touch):
        menu_layout = self.ids.menu_layout
        if self.menu_aberto and menu_layout.opacity > 0:
            if not menu_layout.collide_point(*touch.pos):
                Logger.info("Calculo1: Touch outside open menu detected. Closing menu.")
                self.open_menu()  # Fecha o menu
                return True  # Consome o evento de toque para evitar que outros widgets reajam
            else:
                # Clique dentro do menu, permite que os botões funcionem
                return super().on_touch_down(touch)

        # Fecha a caixa explicativa se clicar fora dela
        if self.explanatory_box and not self.explanatory_box.collide_point(*touch.pos):
            self.close_explanatory_box()
            return True # Consome o evento para evitar que outros widgets reajam
        return super().on_touch_down(touch)

    def show_explanatory_box(self, title, text, image_path, additional_image_path=""):
        if self.explanatory_box and self.explanatory_box.parent:
            self.remove_widget(self.explanatory_box)
            self.explanatory_box = None

        self.explanatory_box = Factory.ExplanatoryBox()
        self.explanatory_box.explanation_title = title

        partes = text.strip().split("***")
        self.explanatory_box.explanation_text_before_image = partes[0].strip() if len(partes) > 0 else ""
        self.explanatory_box.explanation_text_between_images = partes[1].strip() if len(partes) > 1 else ""
        self.explanatory_box.explanation_text_after_images = partes[2].strip() if len(partes) > 2 else ""

        self.explanatory_box.explanation_image_path = image_path
        self.explanatory_box.additional_image_path = additional_image_path

        self.add_widget(self.explanatory_box)

    def update_box(self, *args):
        if self.explanatory_box:
            pass

    def close_explanatory_box(self):
        if self.explanatory_box and self.explanatory_box.parent:
            self.remove_widget(self.explanatory_box)
            self.explanatory_box = None

class Calculo2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False
        self.explanatory_box = None  # Armazena a referência da caixa explicativa

    def on_pre_enter(self, *args):
        # Reseta o estado do menu
        Logger.info("Calculo2: on_pre_enter")
        self.menu_aberto = False
        menu_layout = self.ids.menu_layout

        Animation.cancel_all(menu_layout)
        menu_layout.opacity = 0
        # Garante que a altura seja calculada corretamente
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        menu_layout.pos = (Window.width, target_y_top)

        menu_layout.disabled = True
        Logger.info(f"Calculo2: on_pre_enter - Initial menu pos set to: {menu_layout.pos}")

        # Fecha a caixa explicativa, se estiver aberta
        self.close_explanatory_box()

        # Limpa os campos de entrada
        self.ids.input_5.text = ""
        self.ids.input_6.text = ""
        self.ids.input_7.text = ""
        self.ids.input_8.text = ""
        self.ids.input_9.text = ""

    def _on_menu_close_complete(self, animation, widget):
        Logger.info(f"Calculo2: Menu close animation complete. Disabling widget: {widget}")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        """Chamado quando a animação de abrir o menu termina."""
        Logger.info(f"Calculo2: Menu open animation complete for widget: {widget}")

    def open_menu(self):
        menu_layout = self.ids.menu_layout

        Logger.info(f"Calculo2: open_menu called. Current menu_aberto: {self.menu_aberto}")
        Logger.info(
            f"Calculo2: menu_layout initial - pos: {menu_layout.pos}, size: {menu_layout.size}, opacity: {menu_layout.opacity}, disabled: {menu_layout.disabled}")
        Logger.info(
            f"Calculo2: Window.width: {Window.width}, menu_layout.width: {menu_layout.width}, Window.height: {Window.height}, menu_layout.height: {menu_layout.height}")

        Animation.cancel_all(menu_layout)

        # A largura do menu deve ser (size_hint_x * parent.width).
        current_menu_width = menu_layout.width
        if current_menu_width == 0 and menu_layout.size_hint_x is not None and menu_layout.parent:
            calculated_width = menu_layout.size_hint_x * menu_layout.parent.width
            Logger.warning(
                f"Calculo2: menu_layout.width is 0! Using calculated width based on size_hint: {calculated_width}. This might indicate a timing issue.")
            current_menu_width = calculated_width # Usa a largura calculada

        target_x_open = Window.width - current_menu_width
        off_screen_x = Window.width

        # Garante que a altura seja pega do minimum_height
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        Logger.info(
            f"Calculo2: open_menu - menu_layout.minimum_height: {menu_layout.minimum_height}, Window.height: {Window.height}, target_y_top: {target_y_top}")

        Logger.info(
            f"Calculo2: Calculated animation positions - target_x_open: {target_x_open}, off_screen_x: {off_screen_x}, target_y_top: {target_y_top}")

        if self.menu_aberto:  # Se o menu está aberto, vamos fechá-lo
            Logger.info("Calculo2: Closing menu...")
            anim = Animation(pos=(off_screen_x, target_y_top), opacity=0, duration=0.2)
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False  # Atualiza o estado
        else:  # Se o menu está fechado, vamos abri-lo
            Logger.info("Calculo2: Opening menu...")
            menu_layout.disabled = False  # Habilita antes da animação
            anim = Animation(pos=(target_x_open, target_y_top), opacity=1, duration=0.2)
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True  # Atualiza o estado

        anim.start(menu_layout)
        Logger.info(
            f"Calculo2: Animation started. New menu_aberto: {self.menu_aberto}. Target widget: {menu_layout}")

    def on_touch_down(self, touch):
        menu_layout = self.ids.menu_layout
        if self.menu_aberto and menu_layout.opacity > 0:
            if not menu_layout.collide_point(*touch.pos):
                Logger.info("Calculo2: Touch outside open menu detected. Closing menu.")
                self.open_menu()  # Fecha o menu
                return True
            else:
                return super().on_touch_down(touch)

        if self.explanatory_box and not self.explanatory_box.collide_point(*touch.pos):
            self.close_explanatory_box()
            return True  # Consome o evento para evitar que outros widgets reajam

        return super().on_touch_down(touch)

    def show_explanatory_box(self):
        if self.explanatory_box:  # Se a caixa já estiver aberta, não cria outra
            return

        self.explanatory_box = Factory.ExplanatoryBox()
        self.add_widget(self.explanatory_box)

    def update_box(self, *args):
        if self.explanatory_box:
            pass  # Deixado como pass se não for usado diretamente aqui

    def close_explanatory_box(self):
        if self.explanatory_box:
            self.remove_widget(self.explanatory_box)
            self.explanatory_box = None

    def atualizar_unidade_tempo_pulsada(self, estado):
        if estado == 'down':
            self.ids.input_7_label.text = "Tempo Pulsada (ms)"
        else:
            self.ids.input_7_label.text = "Tempo Pulsada (s)"

    def atualizar_unidade_tempo_base(self, estado):
        if estado == 'down':
            self.ids.input_9_label.text = "Tempo Base (ms)"
        else:
            self.ids.input_9_label.text = "Tempo Base (s)"

class Calculo3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False
        self.explanatory_box = None
        # Não precisamos mais de 'bound_widgets' ou 'bound_toggle_buttons'
        # porque os binds de unidade são no KV e o cálculo é só no botão.

    # Usaremos on_pre_enter, como no Calculo2, para limpar a tela.
    def on_pre_enter(self, *args):
        Logger.info("Calculo3: on_pre_enter")
        # Reseta o estado do menu (lógica similar ao Calculo2)
        self.menu_aberto = False
        if 'menu_layout' in self.ids:
            menu_layout = self.ids.menu_layout
            Animation.cancel_all(menu_layout)
            menu_layout.opacity = 0
            # Garante que a altura seja calculada corretamente
            menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
            target_y_top = Window.height - menu_height
            menu_layout.pos = (Window.width, target_y_top)
            menu_layout.disabled = True
            Logger.info(f"Calculo3: on_pre_enter - Initial menu pos set to: {menu_layout.pos}")

        # Fecha a caixa explicativa, se estiver aberta
        self.close_explanatory_box()

        # LIMPAR TODOS OS CAMPOS AQUI, COMO NO CALCULO2
        Logger.info("Calculo3: Clearing input fields on on_pre_enter.")
        self.ids.input_12.text = ""
        self.ids.input_14.text = ""
        self.ids.input_15.text = ""
        self.ids.input_16.text = ""
        self.ids.input_ief.text = "" # Limpa o campo de resultado também

        # Resetar botões 'ms' para o estado 'normal' (equivalente a segundos) e atualizar labels
        if 'ms_button_tp_id' in self.ids:
            self.ids.ms_button_tp_id.state = 'normal'
            self.ids.input_14_label.text = "Tempo Pulsada (s)"
        if 'ms_button_tb_id' in self.ids:
            self.ids.ms_button_tb_id.state = 'normal'
            self.ids.input_16_label.text = "Tempo Base (s)"

    # Os métodos open_menu, on_touch_down, show_explanatory_box, close_explanatory_box,
    # _on_menu_close_complete, _on_menu_open_complete são mantidos como na sua versão
    # do Calculo2, pois funcionam bem.
    def _on_menu_close_complete(self, animation, widget):
        Logger.info(f"Calculo3: Menu close animation complete. Disabling widget: {widget}")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        Logger.info(f"Calculo3: Menu open animation complete for widget: {widget}")

    def open_menu(self):
        if 'menu_layout' not in self.ids:
            Logger.error("Calculo3: menu_layout not found in self.ids.")
            return

        menu_layout = self.ids.menu_layout
        Logger.info(f"Calculo3: open_menu called. Current menu_aberto: {self.menu_aberto}")

        Animation.cancel_all(menu_layout)

        current_menu_width = menu_layout.width
        if current_menu_width == 0 and menu_layout.size_hint_x is not None and menu_layout.parent:
            calculated_width = menu_layout.size_hint_x * menu_layout.parent.width
            Logger.warning(
                f"Calculo3: menu_layout.width is 0! Using calculated width based on size_hint: {calculated_width}. This might indicate a timing issue.")
            current_menu_width = calculated_width

        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        target_x_open = Window.width - current_menu_width
        off_screen_x = Window.width

        if self.menu_aberto:
            Logger.info("Calculo3: Closing menu...")
            anim = Animation(pos=(off_screen_x, target_y_top), opacity=0, duration=0.2)
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False
        else:
            Logger.info("Calculo3: Opening menu...")
            menu_layout.disabled = False
            anim = Animation(pos=(target_x_open, target_y_top), opacity=1, duration=0.2)
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True

        anim.start(menu_layout)

    def on_touch_down(self, touch):
        if 'menu_layout' in self.ids:
            menu_layout = self.ids.menu_layout
            if self.menu_aberto and menu_layout.opacity > 0:
                if not menu_layout.collide_point(*touch.pos):
                    Logger.info("Calculo3: Touch outside open menu detected. Closing menu.")
                    self.open_menu()
                    return True
        if self.explanatory_box and not self.explanatory_box.collide_point(*touch.pos):
            self.close_explanatory_box()
            return True
        return super().on_touch_down(touch)

    def show_explanatory_box(self, title, text, image_path):
        if self.explanatory_box:
            return
        self.explanatory_box = Factory.ExplanatoryBox()
        self.explanatory_box.explanation_title = title
        self.explanatory_box.explanation_text_before_image = text
        self.explanatory_box.explanation_image_path = image_path

        # Limpa os campos que não serão usados (para não exibir lixo antigo de outra tela)
        self.explanatory_box.explanation_text_between_images = ""
        self.explanatory_box.explanation_text_after_additional_image = ""
        self.explanatory_box.additional_image_path = ""

        self.add_widget(self.explanatory_box)

    def update_box(self, *args):
        if self.explanatory_box:
            pass

    def close_explanatory_box(self):
        if self.explanatory_box:
            self.remove_widget(self.explanatory_box)
            self.explanatory_box = None

    def atualizar_unidade_tempo_pulsada(self, estado):
        if 'input_14_label' in self.ids:
            if estado == 'down':
                self.ids.input_14_label.text = "Tempo Pulsada (ms)"
            else:
                self.ids.input_14_label.text = "Tempo Pulsada (s)"
        # NÃO CHAMA atualizar_saida AQUI! O botão "Calcular" fará isso.

    def atualizar_unidade_tempo_base(self, estado):
        if 'input_16_label' in self.ids:
            if estado == 'down':
                self.ids.input_16_label.text = "Tempo Base (ms)"
            else:
                self.ids.input_16_label.text = "Tempo Base (s)"
        # NÃO CHAMA atualizar_saida AQUI! O botão "Calcular" fará isso.

    def mostrar_erro(self, mensagem):
        self.ids.erro_corrente_efetiva.text = mensagem

    def limpar_erro(self):
        self.ids.erro_corrente_efetiva.text = ""

    def atualizar_saida(self):
        Logger.info("Calculo3: Botão 'Calcular' pressionado. Iniciando cálculo.")

        field_ids = {
            "Ip": "input_12",
            "tp": "input_14",
            "Ib": "input_15",
            "tb": "input_16",
            "Ief": "input_ief",
        }

        input_values = {}
        empty_field_name = None

        for name, obj_id in field_ids.items():
            field_obj = self.ids.get(obj_id)
            if not field_obj:
                Logger.error(f"Calculo3: Widget com ID '{obj_id}' não encontrado.")
                self.mostrar_erro("Erro interno: Widget não encontrado")
                return

            text_value = field_obj.text.replace(",", ".").strip()

            if text_value == "":
                if empty_field_name is None:
                    empty_field_name = name
                else:
                    self.mostrar_erro("Mais de 1 campo vazio!")
                    return
            else:
                try:
                    val = float(text_value)
                    if name in ["tp", "tb"]:
                        ms_button_id = "ms_button_tp_id" if name == "tp" else "ms_button_tb_id"
                        ms_button = self.ids.get(ms_button_id)
                        if ms_button and ms_button.state == 'down':
                            val /= 1000.0
                    input_values[name] = val
                except ValueError:
                    self.mostrar_erro(f"Valor inválido no campo {obj_id}")
                    return

        if empty_field_name is None:
            self.mostrar_erro("Deixe 1 campo vazio")
            return

        try:
            if empty_field_name == "Ief":
                Ip = input_values["Ip"]
                tp = input_values["tp"]
                Ib = input_values["Ib"]
                tb = input_values["tb"]

                numerator = (Ip ** 2 * tp) + (Ib ** 2 * tb)
                denominator = tp + tb

                if denominator == 0:
                    self.mostrar_erro("Erro: t_p + t_b = 0")
                    return
                if numerator < 0:
                    self.mostrar_erro("Erro: Raiz de número negativo")
                    return

                result = math.sqrt(numerator / denominator)
                self.ids.input_ief.text = f"{result:.2f}"
                self.limpar_erro()

            elif empty_field_name == "Ip":
                Ief = input_values["Ief"]
                tp = input_values["tp"]
                Ib = input_values["Ib"]
                tb = input_values["tb"]

                numerator = (Ief ** 2 * (tp + tb)) - (Ib ** 2 * tb)
                denominator = tp

                if denominator == 0:
                    self.mostrar_erro("Erro: t_p = 0")
                    return
                if numerator < 0:
                    self.mostrar_erro("Erro: Raiz de número negativo")
                    return

                result = math.sqrt(numerator / denominator)
                self.ids.input_12.text = f"{result:.2f}"
                self.limpar_erro()

            elif empty_field_name == "Ib":
                Ief = input_values["Ief"]
                tp = input_values["tp"]
                Ip = input_values["Ip"]
                tb = input_values["tb"]

                numerator = (Ief ** 2 * (tp + tb)) - (Ip ** 2 * tp)
                denominator = tb

                if denominator == 0:
                    self.mostrar_erro("Erro: t_b = 0")
                    return
                if numerator < 0:
                    self.mostrar_erro("Erro: Raiz de número negativo")
                    return

                result = math.sqrt(numerator / denominator)
                self.ids.input_15.text = f"{result:.2f}"
                self.limpar_erro()

            elif empty_field_name == "tp":
                Ief = input_values["Ief"]
                Ip = input_values["Ip"]
                Ib = input_values["Ib"]
                tb = input_values["tb"]

                numerator = tb * (Ib ** 2 - Ief ** 2)
                denominator = Ief ** 2 - Ip ** 2

                if denominator == 0:
                    self.mostrar_erro("Erro: Ief² - Ip² = 0")
                    return

                temp_result = numerator / denominator
                if temp_result < 0:
                    self.mostrar_erro("Erro: Tempo negativo")
                    return

                result = temp_result
                if self.ids.get("ms_button_tp_id") and self.ids.ms_button_tp_id.state == 'down':
                    result *= 1000.0

                self.ids.input_14.text = f"{result:.2f}"
                self.limpar_erro()

            elif empty_field_name == "tb":
                Ief = input_values["Ief"]
                Ip = input_values["Ip"]
                Ib = input_values["Ib"]
                tp = input_values["tp"]

                numerator = tp * (Ip ** 2 - Ief ** 2)
                denominator = Ief ** 2 - Ib ** 2

                if denominator == 0:
                    self.mostrar_erro("Erro: Ief² - Ib² = 0")
                    return

                temp_result = numerator / denominator
                if temp_result < 0:
                    self.mostrar_erro("Erro: Tempo negativo")
                    return

                result = temp_result
                if self.ids.get("ms_button_tb_id") and self.ids.ms_button_tb_id.state == 'down':
                    result *= 1000.0

                self.ids.input_16.text = f"{result:.2f}"
                self.limpar_erro()

        except ValueError as ve:
            Logger.error(f"Calculo3: Erro de valor durante o cálculo para {empty_field_name}: {ve}")
            self.mostrar_erro("Erro: Dados insuficientes ou inválidos")

        except Exception as e:
            Logger.error(f"Calculo3: Erro inesperado durante o cálculo de {empty_field_name}: {e}")
            self.mostrar_erro("Erro geral")

class Calculo4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False
        self.explanatory_box = None

    def on_pre_enter(self, *args):
        Logger.info("Calculo4: on_pre_enter")
        self.menu_aberto = False

        if 'menu_layout' in self.ids:
            menu_layout = self.ids.menu_layout
            Animation.cancel_all(menu_layout)
            menu_layout.opacity = 0
            menu_layout.pos = (Window.width, Window.height - menu_layout.height)
            menu_layout.disabled = True

        self.close_explanatory_box()

        Logger.info("Calculo4: Clearing input fields on on_pre_enter.")
        self.ids.input_vs.text = ""
        self.ids.input_freq.text = ""
        self.ids.input_s.text = ""
        self.ids.erro_saida.text = ""

        # Garante que os textos digitados fiquem visíveis (preto)
        for campo in [self.ids.input_vs, self.ids.input_freq, self.ids.input_s]:
            campo.foreground_color = (0, 0, 0, 1)

    def _on_menu_close_complete(self, animation, widget):
        Logger.info(f"Calculo4: Menu close animation complete. Disabling widget: {widget}")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        Logger.info(f"Calculo4: Menu open animation complete for widget: {widget}")

    def open_menu(self):
        if 'menu_layout' not in self.ids:
            Logger.error("Calculo4: menu_layout not found in self.ids.")
            return

        menu_layout = self.ids.menu_layout
        Logger.info(f"Calculo4: open_menu called. Current menu_aberto: {self.menu_aberto}")

        Animation.cancel_all(menu_layout)
        menu_width = menu_layout.width if menu_layout.width else menu_layout.size_hint_x * menu_layout.parent.width
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y = Window.height - menu_height
        off_x = Window.width
        target_x = Window.width - menu_width

        if self.menu_aberto:
            Logger.info("Calculo4: Closing menu...")
            anim = Animation(pos=(off_x, target_y), opacity=0, duration=0.2)
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False
        else:
            Logger.info("Calculo4: Opening menu...")
            menu_layout.disabled = False
            anim = Animation(pos=(target_x, target_y), opacity=1, duration=0.2)
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True
        anim.start(menu_layout)

    def on_touch_down(self, touch):
        if 'menu_layout' in self.ids:
            menu_layout = self.ids.menu_layout
            if self.menu_aberto and menu_layout.opacity > 0 and not menu_layout.collide_point(*touch.pos):
                Logger.info("Calculo4: Touch outside menu. Closing menu.")
                self.open_menu()
                return True

        if self.explanatory_box and not self.explanatory_box.collide_point(*touch.pos):
            self.close_explanatory_box()
            return True

        return super().on_touch_down(touch)

    def show_explanatory_box(self, title, text, image_path):
        if self.explanatory_box:
            return

        self.explanatory_box = Factory.ExplanatoryBox()
        self.explanatory_box.explanation_title = title
        self.explanatory_box.explanation_text_before_image = text
        self.explanatory_box.explanation_image_path = image_path
        self.explanatory_box.explanation_text_between_images = ""
        self.explanatory_box.explanation_text_after_additional_image = ""
        self.explanatory_box.additional_image_path = ""

        self.add_widget(self.explanatory_box)

    def close_explanatory_box(self):
        if self.explanatory_box:
            self.remove_widget(self.explanatory_box)
            self.explanatory_box = None

    def mostrar_erro(self, mensagem):
        self.ids.erro_saida.text = mensagem

    def limpar_erro(self):
        self.ids.erro_saida.text = ""

    def atualizar_saida(self):
        Logger.info("Calculo4: Botão 'Calcular' pressionado. Iniciando cálculo.")
        ids = self.ids

        campos = {
            "s": ids.input_s,
            "vs": ids.input_vs,
            "f": ids.input_freq
        }

        valores = {}
        campo_vazio = None

        for nome, campo in campos.items():
            texto = campo.text.replace(",", ".").strip()
            if texto == "":
                if campo_vazio:
                    self.mostrar_erro("Deixe apenas 1 campo vazio")
                    return
                campo_vazio = nome
            else:
                try:
                    valores[nome] = float(texto)
                except ValueError:
                    self.mostrar_erro(f"Valor inválido em {nome.upper()}")
                    return

        if not campo_vazio:
            self.mostrar_erro("Deixe 1 campo vazio")
            return

        try:
            if campo_vazio == "s":
                vs = valores["vs"]
                f = valores["f"]
                if f == 0:
                    self.mostrar_erro("Erro: Frequência = 0")
                    return
                s = (1000 * vs) / (60 * f)
                ids.input_s.text = f"{s:.1f}"

            elif campo_vazio == "vs":
                s = valores["s"]
                f = valores["f"]
                vs = (s * 60 * f) / 1000
                ids.input_vs.text = f"{vs:.1f}"

            elif campo_vazio == "f":
                s = valores["s"]
                vs = valores["vs"]
                if s == 0:
                    self.mostrar_erro("Erro: Deslocamento = 0")
                    return
                f = (1000 * vs) / (60 * s)
                ids.input_freq.text = f"{f:.1f}"
            self.limpar_erro()

        except Exception as e:
            Logger.error(f"Calculo4: Erro inesperado: {e}")
            self.mostrar_erro("Erro no cálculo")

class SimbologiadeSoldagem(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False  # Inicializa o estado do menu
        self.explanatory_box = None

    def on_pre_enter(self, *args):
        # Chamado sempre que a tela está prestes a ser exibida
        Logger.info("SimbologiadeSoldagem: on_pre_enter")
        self.menu_aberto = False
        menu_layout = self.ids.menu_layout # Assumindo que você tem um id 'menu_layout' no seu KV

        # Cancela animações pendentes e redefine o estado inicial do menu
        Animation.cancel_all(menu_layout)
        menu_layout.opacity = 0
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        menu_layout.pos = (Window.width, target_y_top)

        menu_layout.disabled = True
        Logger.info(f"SimbologiadeSoldagem: on_pre_enter - Initial menu pos set to: {menu_layout.pos}")

        self.close_explanatory_box()

    def _on_menu_close_complete(self, animation, widget):
        """Chamado quando a animação de fechar o menu termina."""
        Logger.info(f"SimbologiadeSoldagem: Menu close animation complete. Disabling widget: {widget}")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        """Chamado quando a animação de abrir o menu termina."""
        Logger.info(f"SimbologiadeSoldagem: Menu open animation complete for widget: {widget}")

    def open_menu(self):
        menu_layout = self.ids.menu_layout

        Logger.info(f"SimbologiadeSoldagem: open_menu called. Current menu_aberto: {self.menu_aberto}")
        Logger.info(
            f"SimbologiadeSoldagem: menu_layout initial - pos: {menu_layout.pos}, size: {menu_layout.size}, opacity: {menu_layout.opacity}, disabled: {menu_layout.disabled}")
        Logger.info(f"SimbologiadeSoldagem: Window.width: {Window.width}, menu_layout.width: {menu_layout.width}, Window.height: {Window.height}, menu_layout.height: {menu_layout.height}")

        # Cancela qualquer animação em progresso no menu_layout
        Animation.cancel_all(menu_layout)

        current_menu_width = menu_layout.width
        if current_menu_width == 0 and menu_layout.size_hint_x is not None and menu_layout.parent:
            calculated_width = menu_layout.size_hint_x * menu_layout.parent.width
            Logger.warning(
                f"SimbologiadeSoldagem: menu_layout.width is 0! Using calculated width based on size_hint: {calculated_width}. This might indicate a timing issue.")

        target_x_open = Window.width - current_menu_width
        # Posição X para o menu fechado (borda esquerda do menu fora da tela à direita)
        off_screen_x = Window.width

        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        Logger.info(f"SimbologiadeSoldagem: open_menu - menu_layout.height: {menu_layout.height}, Window.height: {Window.height}, target_y_top: {target_y_top}")

        Logger.info(
            f"SimbologiadeSoldagem: Calculated animation positions - target_x_open: {target_x_open}, off_screen_x: {off_screen_x}, target_y_top: {target_y_top}")

        if self.menu_aberto:  # Se o menu está aberto, vamos fechá-lo
            Logger.info("SimbologiadeSoldagem: Closing menu...")
            anim = Animation(pos=(off_screen_x, target_y_top), opacity=0, duration=0.2)
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False  # Atualiza o estado
        else:  # Se o menu está fechado, vamos abri-lo
            Logger.info("SimbologiadeSoldagem: Opening menu...")
            menu_layout.disabled = False  # Habilita antes da animação
            anim = Animation(pos=(target_x_open, target_y_top), opacity=1, duration=0.2)
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True  # Atualiza o estado

        anim.start(menu_layout)
        Logger.info(
            f"SimbologiadeSoldagem: Animation started. New menu_aberto: {self.menu_aberto}. Target widget: {menu_layout}")

    def on_touch_down(self, touch):
        menu_layout = self.ids.menu_layout
        if self.menu_aberto and menu_layout.opacity > 0:
            if not menu_layout.collide_point(*touch.pos):
                Logger.info("SimbologiadeSoldagem: Touch outside open menu detected. Closing menu.")
                self.open_menu()  # Fecha o menu
                return True  # Consome o evento de toque para evitar que outros widgets reajam
            else:
                return super().on_touch_down(touch)

        if self.explanatory_box and not self.explanatory_box.collide_point(*touch.pos):
            self.close_explanatory_box()
            return True # Consome o evento para evitar que outros widgets reajam

        return super().on_touch_down(touch)

    def show_explanatory_box(self, title, text):
        if self.explanatory_box:
            return

        self.explanatory_box = Factory.ExplanatoryBox()
        self.explanatory_box.explanation_title = title
        self.explanatory_box.explanation_text_before_image = text  # ou divida como no Calculo1 se quiser
        self.explanatory_box.explanation_text_after_image = ""
        self.explanatory_box.explanation_image_path = ""  # ou algum padrão

        self.add_widget(self.explanatory_box)

    def close_explanatory_box(self):
        if self.explanatory_box:
            self.remove_widget(self.explanatory_box)
            self.explanatory_box = None

class Conversor1(Screen):
    input_10 = ObjectProperty(None)
    input_11 = ObjectProperty(None)
    unidade_entrada = ObjectProperty(None)
    unidade_saida = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False

    def on_kv_post(self, base_widget):
        Clock.schedule_once(self._bind_events)

    def inverter_spinners(self):
        # 1. Store current states
        current_input_unit = self.unidade_entrada.text
        current_output_unit = self.unidade_saida.text
        current_input_value = self.input_10.text
        current_output_value = self.input_11.text

        # 2. Swap units
        self.unidade_entrada.text = current_output_unit
        self.unidade_saida.text = current_input_unit

        # 3. Swap values in the text inputs
        self.input_10.text = current_output_value
        self.input_11.text = current_input_value

    def _bind_events(self, *args):
        self.input_10.bind(text=self.atualizar_saida)
        self.unidade_entrada.bind(text=self.atualizar_saida)
        self.unidade_saida.bind(text=self.atualizar_saida)

    def atualizar_saida(self, *args):
        entrada = self.input_10.text.replace(",", ".")
        try:
            valor = float(entrada)
        except ValueError:
            self.input_11.text = ""
            return

        unidade_origem = self.unidade_entrada.text
        unidade_destino = self.unidade_saida.text

        valor_metros = self.converter_para_mps(valor, unidade_origem)

        # Check if conversion to base unit was successful
        if valor_metros is None:
            self.input_11.text = "Erro"
            return

        resultado = self.converter_de_mps(valor_metros, unidade_destino)

        # Only update input_11 if the calculated result is valid
        if resultado is not None:
            self.input_11.text = f"{resultado:.2f}"
        else:
            self.input_11.text = "Erro" # Or handle as desired


    def converter_para_mps(self, valor, unidade):
        if unidade == "mm/s":
            return valor * 0.001
        elif unidade == "cm/min":
            return valor * 0.0001666667
        elif unidade == "in/s":
            return valor * 0.0254
        elif unidade == "m/s":
            return valor
        # Return None or raise an error if unit is not recognized
        return None

    def converter_de_mps(self, valor, unidade):
        if valor is None: # Handle case where conversion to mps failed
            return None
        if unidade == "mm/s":
            return valor / 0.001
        elif unidade == "cm/min":
            return valor / 0.0001666667
        elif unidade == "in/s":
            return valor / 0.0254
        elif unidade == "m/s":
            return valor
        # Return None or raise an error if unit is not recognized
        return None

    def on_pre_enter(self, *args):
        self.menu_aberto = False
        # Assuming you have a menu_layout in your KV, otherwise this part might need adjustment
        if 'menu_layout' in self.ids: # Added a check to avoid KeyError if menu_layout is not defined in KV
            menu_layout = self.ids.menu_layout
            Animation.cancel_all(menu_layout)
            menu_layout.opacity = 0
            menu_layout.disabled = True

            menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
            target_y_top = Window.height - menu_height
            menu_layout.pos = (Window.width, target_y_top)

        # Clear fields when entering the screen
        self.input_10.text = ""
        self.input_11.text = ""
        self.unidade_entrada.text = "mm/s"
        self.unidade_saida.text = "cm/min"


    def _on_menu_close_complete(self, animation, widget):
        Logger.info(f"Conversor1: Menu close complete")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        Logger.info(f"Conversor1: Menu open complete")

    def open_menu(self):
        menu_layout = self.ids.menu_layout
        Animation.cancel_all(menu_layout)

        current_menu_width = menu_layout.width
        if current_menu_width == 0 and menu_layout.size_hint_x and menu_layout.parent:
            current_menu_width = menu_layout.size_hint_x * menu_layout.parent.width

        target_x_open = Window.width - current_menu_width
        off_screen_x = Window.width
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height

        if self.menu_aberto:
            Logger.info("Conversor1: Closing menu...")
            anim = Animation(pos=(off_screen_x, target_y_top), opacity=0, duration=0.2)
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False
        else:
            Logger.info("Conversor1: Opening menu...")
            menu_layout.disabled = False
            anim = Animation(pos=(target_x_open, target_y_top), opacity=1, duration=0.2)
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True

        anim.start(menu_layout)

    def on_touch_down(self, touch):
        menu_layout = self.ids.menu_layout
        if self.menu_aberto and menu_layout.opacity > 0:
            if not menu_layout.collide_point(*touch.pos):
                Logger.info("Conversor1: Toque fora do menu — fechando.")
                self.open_menu()
                return True
        return super().on_touch_down(touch)

class Conversor2(Screen):
    input_12 = ObjectProperty(None) # Este será agora o campo de entrada
    input_13 = ObjectProperty(None) # Este será agora o campo de saída
    unidade_entrada = ObjectProperty(None)
    unidade_saida = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False

    def on_kv_post(self, base_widget):
        """Chamado depois que o arquivo KV é carregado e o widget raiz foi criado."""
        Clock.schedule_once(self._bind_events)

    def inverter_spinners(self):
        """Inverte o texto dos spinners de unidade de entrada e saída."""
        entrada_texto = self.unidade_entrada.text
        saida_texto = self.unidade_saida.text
        self.unidade_entrada.text = saida_texto
        self.unidade_saida.text = entrada_texto
        # Aciona uma atualização após a inversão
        self.atualizar_saida()

    def _bind_events(self, *args):
        # Garantir que input_12 exista antes de associar para evitar AttributeError
        if self.input_12:
            self.input_12.bind(text=self.atualizar_saida)
        if self.unidade_entrada:
            self.unidade_entrada.bind(text=self.atualizar_saida)
        if self.unidade_saida:
            self.unidade_saida.bind(text=self.atualizar_saida)

    def atualizar_saida(self, *args):
        # Agora usando input_12 para a entrada
        entrada = self.input_12.text.replace(",", ".")
        try:
            valor = float(entrada)
        except ValueError:
            # Limpa a saída se a entrada não for um número válido
            # Agora usando input_13 para a saída
            self.input_13.text = ""
            return

        unidade_origem = self.unidade_entrada.text
        unidade_destino = self.unidade_saida.text

        # Converte o valor de entrada para uma unidade base (L/min)
        valor_lpm = self.converter_para_lpm(valor, unidade_origem)
        # Converte da unidade base (L/min) para a unidade de saída desejada
        resultado = self.converter_de_lpm(valor_lpm, unidade_destino)

        # Exibe o resultado formatado com duas casas decimais
        self.input_13.text = f"{resultado:.3f}"

    def converter_para_lpm(self, valor, unidade):
        if unidade == "L/min":
            return valor
        elif unidade == "m³/min":
            return valor * 1000  # 1 metro cúbico = 1000 litros
        Logger.warning(f"Conversor2: Unidade de origem '{unidade}' não reconhecida.")
        return valor # Retorna o valor original se a unidade não for reconhecida

    def converter_de_lpm(self, valor, unidade):
        if unidade == "L/min":
            return valor
        elif unidade == "m³/min":
            return valor / 1000  # 1 litro = 0.001 metros cúbicos
        Logger.warning(f"Conversor2: Unidade de destino '{unidade}' não reconhecida.")
        return valor # Retorna o valor original se a unidade não for reconhecida

    def on_pre_enter(self, *args):
        self.menu_aberto = False
        menu_layout = self.ids.menu_layout # Assume que o id 'menu_layout' existe no KV

        # Cancela qualquer animação em andamento e define o estado inicial do menu
        Animation.cancel_all(menu_layout)
        menu_layout.opacity = 0
        menu_layout.disabled = True

        # Calcula a posição alvo para o menu fora da tela
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        menu_layout.pos = (Window.width, target_y_top)
        # Limpa os campos de entrada e define as unidades padrão para a conversão de vazão de gás
        # Agora usando input_12 e input_13
        if self.input_12:
            self.input_12.text = ""
        if self.input_13:
            self.input_13.text = ""

        if self.unidade_entrada:
            self.unidade_entrada.text = "L/min"
        if self.unidade_saida:
            self.unidade_saida.text = "m³/min"

    def _on_menu_close_complete(self, animation, widget):
        """Callback para quando a animação de fechamento do menu é concluída."""
        Logger.info(f"Conversor2: Fechamento do menu concluído")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        """Callback para quando a animação de abertura do menu é concluída."""
        Logger.info(f"Conversor2: Abertura do menu concluída")

    def open_menu(self):
        """Alterna a visibilidade do menu com uma animação."""
        menu_layout = self.ids.menu_layout
        Animation.cancel_all(menu_layout)

        current_menu_width = menu_layout.width
        if current_menu_width == 0 and menu_layout.size_hint_x and menu_layout.parent:
            current_menu_width = menu_layout.size_hint_x * menu_layout.parent.width

        target_x_open = Window.width - current_menu_width
        off_screen_x = Window.width
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height

        if self.menu_aberto:
            Logger.info("Conversor2: Fechando menu...")
            anim = Animation(pos=(off_screen_x, target_y_top), opacity=0, duration=0.2)
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False
        else:
            Logger.info("Conversor2: Abrindo menu...")
            menu_layout.disabled = False
            anim = Animation(pos=(target_x_open, target_y_top), opacity=1, duration=0.2)
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True

        anim.start(menu_layout)

    def on_touch_down(self, touch):
        """Lida com eventos de toque para fechar o menu se tocado fora."""
        menu_layout = self.ids.menu_layout
        if self.menu_aberto and menu_layout.opacity > 0:
            if not menu_layout.collide_point(*touch.pos):
                Logger.info("Conversor2: Toque fora do menu — fechando.")
                self.open_menu()
                return True # Consome o evento de toque
        return super().on_touch_down(touch)

class ConversordeUnidades(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_aberto = False

    def on_pre_enter(self, *args):
        # Chamado sempre que a tela está prestes a ser exibida
        Logger.info("ConversordeUnidades: on_pre_enter")
        self.menu_aberto = False
        menu_layout = self.ids.menu_layout

        Animation.cancel_all(menu_layout)
        menu_layout.opacity = 0
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        # Posição inicial fora da tela (à direita, alinhado ao TOPO)
        menu_layout.pos = (Window.width, target_y_top)
        menu_layout.disabled = True
        Logger.info(f"ConversordeUnidades: on_pre_enter - Initial menu pos set to: {menu_layout.pos}")

    def _on_menu_close_complete(self, animation, widget):
        """Chamado quando a animação de fechar o menu termina."""
        Logger.info(f"ConversordeUnidades: Menu close animation complete. Disabling widget: {widget}")
        widget.disabled = True

    def _on_menu_open_complete(self, animation, widget):
        """Chamado quando a animação de abrir o menu termina."""
        Logger.info(f"CalculosdeSoldagem: Menu open animation complete for widget: {widget}")

    def open_menu(self):
        menu_layout = self.ids.menu_layout

        Logger.info(f"CalculosdeSoldagem: open_menu called. Current menu_aberto: {self.menu_aberto}")
        Logger.info(
            f"CalculosdeSoldagem: menu_layout initial - pos: {menu_layout.pos}, size: {menu_layout.size}, opacity: {menu_layout.opacity}, disabled: {menu_layout.disabled}")
        Logger.info(
            f"CalculosdeSoldagem: Window.width: {Window.width}, menu_layout.width: {menu_layout.width}, Window.height: {Window.height}, menu_layout.height: {menu_layout.height}")

        # Cancela qualquer animação em progresso no menu_layout
        Animation.cancel_all(menu_layout)

        # A largura do menu deve ser (size_hint_x * parent.width).
        current_menu_width = menu_layout.width
        if current_menu_width == 0 and menu_layout.size_hint_x is not None and menu_layout.parent:
            calculated_width = menu_layout.size_hint_x * menu_layout.parent.width
            Logger.warning(
                f"ConversordeUnidades: menu_layout.width is 0! Using calculated width based on size_hint: {calculated_width}. This might indicate a timing issue.")
            # If width is 0, the X calculation will be wrong, but let's proceed for the Y part.
        target_x_open = Window.width - current_menu_width
        # Posição X para o menu fechado (borda esquerda do menu fora da tela à direita)
        off_screen_x = Window.width

        # --- MODIFICAÇÃO PARA MANTER A POSIÇÃO Y NO TOPO DURANTE A ANIMAÇÃO ---
        menu_height = menu_layout.height if menu_layout.height > 0 else menu_layout.minimum_height
        target_y_top = Window.height - menu_height
        Logger.info(
            f"ConversordeUnidades: open_menu - menu_layout.height: {menu_layout.height}, Window.height: {Window.height}, target_y_top: {target_y_top}")
        # --- FIM DA MODIFICAÇÃO ---

        Logger.info(
            f"ConversordeUnidades: Calculated animation positions - target_x_open: {target_x_open}, off_screen_x: {off_screen_x}, target_y_top: {target_y_top}")

        if self.menu_aberto:  # Se o menu está aberto, vamos fechá-lo
            Logger.info("CalculosdeSoldagem: Closing menu...")
            # --- MODIFICAÇÃO NA ANIMAÇÃO DE FECHAR ---
            anim = Animation(pos=(off_screen_x, target_y_top), opacity=0, duration=0.2)
            # --- FIM DA MODIFICAÇÃO ---
            anim.bind(on_complete=self._on_menu_close_complete)
            self.menu_aberto = False  # Atualiza o estado
        else:  # Se o menu está fechado, vamos abri-lo
            Logger.info("ConversordeUnidades: Opening menu...")
            menu_layout.disabled = False  # Habilita antes da animação
            # --- MODIFICAÇÃO NA ANIMAÇÃO DE ABRIR ---
            anim = Animation(pos=(target_x_open, target_y_top), opacity=1, duration=0.2)
            # --- FIM DA MODIFICAÇÃO ---
            anim.bind(on_complete=self._on_menu_open_complete)
            self.menu_aberto = True  # Atualiza o estado

        anim.start(menu_layout)
        Logger.info(
            f"ConversordeUnidades: Animation started. New menu_aberto: {self.menu_aberto}. Target widget: {menu_layout}")

    def on_touch_down(self, touch):
        menu_layout = self.ids.menu_layout

        # Verifica se o menu está aberto e se o clique ocorreu fora do menu
        if self.menu_aberto and menu_layout.opacity > 0:
            if not menu_layout.collide_point(*touch.pos):
                Logger.info("CalculosdeSoldagem: Touch outside open menu detected. Closing menu.")
                self.open_menu()  # Fecha o menu
                return True  # Consome o evento de toque para evitar que outros widgets reajam
            else:
                # Clique dentro do menu, permite que os botões funcionem
                return super().on_touch_down(touch)

        # Permite que o clique em outros widgets funcione normalmente
        return super().on_touch_down(touch)

class SobreoLTS(Screen):
    pass

class Contatos(Screen):
    pass

class LTSapp(App):
    def calcula_energia(self):
        try:
            tela = self.root.get_screen("Calculo1")

            def formatar_numero(valor_str):
                valor_str = valor_str.strip()
                if valor_str.count(',') > 1 or valor_str.count('.') > 1:
                    raise ValueError("Formato numérico inválido.")
                return valor_str.replace(",", ".")

            def mostrar_erro(tela, mensagem):
                tela.ids.erro_energia.text = mensagem

            def limpar_erro(tela):
                tela.ids.erro_energia.text = ""

            inputs_text = [
                tela.ids.input_1.text.strip(),  # Energia
                tela.ids.input_2.text.strip(),  # Tensão
                tela.ids.input_3.text.strip(),  # Corrente
                tela.ids.input_4.text.strip()  # Velocidade
            ]

            valores_str_formatted = [formatar_numero(v) if v else None for v in inputs_text]
            valores_float = []
            for v_str in valores_str_formatted:
                if v_str is None:
                    valores_float.append(None)
                else:
                    try:
                        valores_float.append(float(v_str))
                    except ValueError:
                        raise ValueError("Um ou mais valores numéricos fornecidos são inválidos.")

            energia, tensao, corrente, velocidade = valores_float

            campos_vazios = valores_float.count(None)
            if campos_vazios == 0:
                raise ValueError("Deixe 1 campo vazio")
            elif campos_vazios > 1:
                raise ValueError("Deixe 1 campo vazio")

            fator_j_para_kj = 1000

            if energia is None:
                if tensao is None or corrente is None or velocidade is None:
                    raise ValueError("Preencha Tensão, Corrente e Velocidade.")
                if velocidade == 0:
                    raise ValueError("A velocidade não pode ser zero.")

                energia_joule_mm = (tensao * corrente * 6) / velocidade
                energia_kj_mm = energia_joule_mm / fator_j_para_kj
                tela.ids.input_1.text = f"{energia_kj_mm:.3f}".replace(".", ",")
                limpar_erro(tela)

            else:
                energia_joule_mm = energia * fator_j_para_kj

                if tensao is None:
                    if corrente is None or velocidade is None:
                        raise ValueError("Preencha Energia, Corrente e Velocidade.")
                    if corrente == 0 or energia_joule_mm == 0:
                        raise ValueError("Corrente ou Energia não podem ser zero.")
                    tensao = (energia_joule_mm * velocidade) / (corrente * 6)
                    tela.ids.input_2.text = f"{tensao:.1f}".replace(".", ",")
                    limpar_erro(tela)

                elif corrente is None:
                    if tensao is None or velocidade is None:
                        raise ValueError("Preencha Energia, Tensão e Velocidade.")
                    if tensao == 0 or energia_joule_mm == 0:
                        raise ValueError("Tensão ou Energia não podem ser zero.")
                    corrente = (energia_joule_mm * velocidade) / (tensao * 6)
                    tela.ids.input_3.text = f"{corrente:.1f}".replace(".", ",")
                    limpar_erro(tela)

                elif velocidade is None:
                    if tensao is None or corrente is None:
                        raise ValueError("Preencha Energia, Tensão e Corrente.")
                    if energia_joule_mm == 0:
                        raise ValueError("Energia não pode ser zero.")
                    velocidade = (tensao * corrente * 6) / energia_joule_mm
                    tela.ids.input_4.text = f"{velocidade:.2f}".replace(".", ",")
                    limpar_erro(tela)

        except ValueError as e:
            Logger.error(f"CalculosdeSoldagem: Erro de validação ou cálculo: {e}")
            mostrar_erro(tela, str(e) if str(e) else "Erro no cálculo")

        except Exception as e:
            Logger.error(f"CalculosdeSoldagem: Erro inesperado durante o cálculo: {e}")
            mostrar_erro(tela, "Erro inesperado")

    def calcula_corrente_pulsada(self):
        try:
            tela = self.root.get_screen("Calculo2")
            use_ms_tp = tela.ids.ms_button_tp.state == 'down'
            use_ms_tb = tela.ids.ms_button_tb.state == 'down'

            def formatar_numero(valor_str):
                valor_str = valor_str.strip()
                if valor_str.count(',') > 1 or valor_str.count('.') > 1:
                    raise ValueError("Formato numérico inválido.")
                # Allow empty string to be handled later as None
                if not valor_str:
                    return None
                return float(valor_str.replace(",", "."))

            def mostrar_erro_temporario(tela, mensagem):
                tela.ids.erro_corrente.text = mensagem

            def limpar_erro(tela):
                tela.ids.erro_corrente.text = ""

            def converter_para_segundos(valor_float_or_none, is_ms_active):
                if valor_float_or_none is None:
                    return None
                return valor_float_or_none / 1000 if is_ms_active else valor_float_or_none

            cm = formatar_numero(tela.ids.input_5.text)
            cp = formatar_numero(tela.ids.input_6.text)
            tp = formatar_numero(tela.ids.input_7.text)
            cb = formatar_numero(tela.ids.input_8.text)
            tb = formatar_numero(tela.ids.input_9.text)
            tp_calc_unit = converter_para_segundos(tp, use_ms_tp)
            tb_calc_unit = converter_para_segundos(tb, use_ms_tb)

            campos_vazios = [v is None for v in [cm, cp, tp, cb, tb]].count(True)

            if campos_vazios == 0:
                raise ValueError("Deixe 1 campo vazio")
            if campos_vazios > 1:
                raise ValueError("Deixe 1 campo vazio")

            if cm is None:
                if tp_calc_unit is not None and tb_calc_unit is not None and cp is not None and cb is not None:
                    if (tp_calc_unit + tb_calc_unit) == 0:
                        raise ValueError("A soma dos tempos não pode ser 0")
                    cm_calc = ((cp * tp_calc_unit) + (cb * tb_calc_unit)) / (tp_calc_unit + tb_calc_unit)
                    tela.ids.input_5.text = f"{cm_calc:.2f}".replace(".", ",")
                    limpar_erro(tela)
            elif cp is None:
                if tp_calc_unit is not None and tb_calc_unit is not None and cm is not None and cb is not None:
                    if tp_calc_unit == 0:
                        raise ValueError("Tempo Pulsada não pode ser 0")
                    cp_calc = (cm * (tp_calc_unit + tb_calc_unit) - cb * tb_calc_unit) / tp_calc_unit
                    tela.ids.input_6.text = f"{cp_calc:.2f}".replace(".", ",")
                    limpar_erro(tela)
            elif tp is None: # Corrected variable name from tempo_pulsada
                if tb_calc_unit is not None and cm is not None and cp is not None and cb is not None:
                    if (cm - cp) == 0:
                        raise ValueError("Corrente Média e Corrente Pulsada não podem ser iguais")
                    tp_calc = (tb_calc_unit * (cb - cm)) / (cm - cp)
                    if use_ms_tp:
                        tela.ids.input_7.text = f"{tp_calc * 1000:.2f}".replace(".", ",")
                    else:
                        tela.ids.input_7.text = f"{tp_calc:.2f}".replace(".", ",")
                        limpar_erro(tela)
            elif cb is None: # Corrected variable name from corrente_base
                if tp_calc_unit is not None and tb_calc_unit is not None and cm is not None and cp is not None:
                    if tb_calc_unit == 0:
                        raise ValueError("Tempo Base não pode ser 0")
                    cb_calc = (cm * (tp_calc_unit + tb_calc_unit) - cp * tp_calc_unit) / tb_calc_unit
                    tela.ids.input_8.text = f"{cb_calc:.2f}".replace(".", ",")
                    limpar_erro(tela)
            elif tb is None: # Corrected variable name from tempo_base
                if tp_calc_unit is not None and cm is not None and cb is not None and cp is not None:
                    if (cm - cb) == 0:
                        raise ValueError("Corrente Média e Corrente Base não podem ser iguais")
                    tb_calc = (tp_calc_unit * (cp - cm)) / (cm - cb)
                    # Convert back to milliseconds if ms button is active for display
                    if use_ms_tb:
                        tela.ids.input_9.text = f"{tb_calc * 1000:.2f}".replace(".", ",")
                    else:
                        tela.ids.input_9.text = f"{tb_calc:.2f}".replace(".", ",")
                        limpar_erro(tela)

        except ValueError as e:
            Logger.error(f"CalculosdeSoldagem: Erro de validação ou cálculo de Corrente Pulsada: {e}")
            error_msg = str(e) if str(e) else "Erro no cálculo"
            # Assign error message only to the field that was supposed to be calculated
            if cm is None: mostrar_erro_temporario(tela, error_msg)
            elif cp is None: tela.ids.input_6.text = error_msg
            elif tp is None: tela.ids.input_7.text = error_msg
            elif cb is None: tela.ids.input_8.text = error_msg
            elif tb is None: tela.ids.input_9.text = error_msg
            else: # General validation error (e.g., more than one empty field)
                tela.ids.erro_corrente.text = error_msg
                tela.ids.input_6.text = error_msg
                tela.ids.input_7.text = error_msg
                tela.ids.input_8.text = error_msg
                tela.ids.input_9.text = error_msg
        except Exception as e:
            Logger.error(f"CalculosdeSoldagem: Erro inesperado durante o cálculo de Corrente Pulsada: {e}")
            tela.ids.input_5.text = "Erro"
            tela.ids.input_6.text = "Erro"
            tela.ids.input_7.text = "Erro"
            tela.ids.input_8.text = "Erro"
            tela.ids.input_9.text = "Erro"

    def build(self):
        return GerenciadorTelas()

LTSapp().run()
