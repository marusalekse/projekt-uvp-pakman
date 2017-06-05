import tkinter as tk
import model

SKALA = 20
BARVA_STENE = '#003'
BARVA_PAKMANA = '#EE0'
KORAK_MS = 30

VELIKOST_CEKINA = SKALA / 5
BARVA_CEKINA = "#00A"

VELIKOST_BOMBONA = SKALA / 3
BARVA_BOMBONA = "#FF0"

class Igra:
  def __init__(self, okno, ime_povrsine):
    self.igra = model.Igra(ime_povrsine)
    self.koraki = 0
    self.cas=0
    self.okno = okno
    self.plosca = tk.Canvas(
        width=SKALA * self.igra.povrsina.sirina,
        height=SKALA * self.igra.povrsina.visina
    )
    self.okno.bind('<Key>', self.obdelaj_tipko)
    self.plosca.pack()
    self.narisi()
    self.okno.after(KORAK_MS, self.korak)

  def koncaj(self, sporocilo):
    self.okno.destroy()
    koncno_okno = tk.Tk()
    sporocilo = tk.Label(koncno_okno, text="{}! Vaš rezultat: {}".format(sporocilo, self.igra.rezultat))
    sporocilo.pack()
    koncno_okno.mainloop()
    return

  def korak(self):
    if(len(self.igra.povrsina.bomboni) == 0 and len(self.igra.povrsina.cekini) == 0):
      self.koncaj("Zmaga")
    self.koraki += 1
    nadaljuj_igro = self.igra.korak()
    if not nadaljuj_igro:
      self.koncaj("Poraz")
    else:
      self.narisi()
      self.okno.after(KORAK_MS, self.korak)
    

  def obdelaj_tipko(self, event):
    if event.keysym == 'Right':
        self.igra.spremeni_smer(model.DESNO)
    elif event.keysym == 'Left':
        self.igra.spremeni_smer(model.LEVO)
    elif event.keysym == 'Up':
        self.igra.spremeni_smer(model.GOR)
    elif event.keysym == 'Down':
        self.igra.spremeni_smer(model.DOL)
    self.narisi()

  def narisi(self):
    self.plosca.delete('all')
    for y_celice in range(self.igra.povrsina.visina):
      for x_celice in range(self.igra.povrsina.sirina):
        if self.igra.povrsina.tabela[y_celice][x_celice] == model.POLJE_ZID:
          self.plosca.create_rectangle(
            x_celice * SKALA,
            y_celice * SKALA,
            (x_celice + 1) * SKALA,
            (y_celice + 1) * SKALA,
            fill = BARVA_STENE,
            outline = BARVA_STENE
          )
    for cekin in self.igra.povrsina.cekini:
      x_cekina, y_cekina = cekin
      self.plosca.create_rectangle(
        x_cekina * SKALA + (SKALA - VELIKOST_CEKINA) / 2,
        y_cekina * SKALA + (SKALA - VELIKOST_CEKINA) / 2,
        (x_cekina + 1) * SKALA - (SKALA - VELIKOST_CEKINA) / 2,
        (y_cekina + 1) * SKALA - (SKALA - VELIKOST_CEKINA) / 2,
        fill = BARVA_CEKINA,
        outline = BARVA_CEKINA
      )

    for bombon in self.igra.povrsina.bomboni:
      x_bombona, y_bombona = bombon
      self.plosca.create_rectangle(
        x_bombona * SKALA + (SKALA - VELIKOST_BOMBONA) / 2,
        y_bombona * SKALA + (SKALA - VELIKOST_BOMBONA) / 2,
        (x_bombona + 1) * SKALA - (SKALA - VELIKOST_BOMBONA) / 2,
        (y_bombona + 1) * SKALA - (SKALA - VELIKOST_BOMBONA) / 2,
        fill = BARVA_BOMBONA,
        outline = BARVA_BOMBONA
      )

    for duhec in self.igra.duhci:
        duhec_x, duhec_y = duhec.pozicija
        zacetek = self.cas
        barva = BARVA_CEKINA
        #if (self.igra.obratna_igra == False or self.cas - zacetek > 10):
        #  barva = BARVA_CEKINA
        #elif self.cas % 6 < 4 :
        #  barva = BARVA_BOMBONA
        #else:
        #  barva = '#0E0'
        self.plosca.create_oval(
          duhec_x * SKALA,
          duhec_y * SKALA,
          (duhec_x + 1) * SKALA,
          (duhec_y + 1) * SKALA,
          fill = barva,
          outline = BARVA_CEKINA
        )
        self.cas += 1


    pakman_x, pakman_y = self.igra.pakman.pozicija
    self.plosca.create_oval(
      pakman_x * SKALA,
      pakman_y * SKALA,
      (pakman_x + 1) * SKALA,
      (pakman_y + 1) * SKALA,
        fill = BARVA_PAKMANA,
        outline = BARVA_PAKMANA
      )


      


okno = tk.Tk()
moj_program = Igra(okno, 'povrsine/povrsina1.pak')
okno.mainloop()