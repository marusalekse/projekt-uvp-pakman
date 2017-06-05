#!/usr/bin/env python3.5
import random
import math
DESNO, GOR, DOL, LEVO= 'desno', 'gor', 'dol', 'levo'
POLJE_PRAZNO, POLJE_ZID = 0, 1
DOLZINA_KORAKA = 0.1

class Pakman:
  #za pakmana dolocimo kje je in kaj je njegova smer, 
  #ima funkciji za nastavitev smeri in premik
  def __init__(self, pozicija):
    #kje se nahaja
    self.pozicija = pozicija

  def nastavi_smer(self, smer):
    self.smer = smer

  def premik(self):
    x, y = self.pozicija
    if self.smer == DESNO:
      x = x + DOLZINA_KORAKA
    elif self.smer == LEVO:
      x = x - DOLZINA_KORAKA
    elif self.smer == GOR:
      y = y - DOLZINA_KORAKA
    elif self.smer == DOL:
      y = y + DOLZINA_KORAKA
    self.pozicija = (x, y)

  def premik_kam(self, smer):
    x, y = self.pozicija
    if smer == DESNO:
      x = x + 1
    elif smer == LEVO:
      x = x - 1
    elif smer == GOR:
      y = y - 1
    elif smer == DOL:
      y = y + 1
    return (x, y)

class Povrsina:
  #iz datoteke z mapo prebere katera polja so kaj
  def __init__(self, ime_povrsine):
    self.tabela = []
    self.portali = {}
    self.cekini = []
    self.bomboni = []
    self.duhci = []
    x_koordinata, y_koordinata = 0, 0
    stevilo_vrstice = 0
    with open(ime_povrsine) as f:
      for vrstica in f:
        x_koordinata = 0
        self.tabela.append([])
        vrstica = vrstica.strip()
        for znak in vrstica:
          # Prazno ali zid
          if znak == '0' or znak == '1':
            self.tabela[stevilo_vrstice].append(int(znak))
          # Portali
          elif znak >= 'A' and znak <= 'Z':
            self.tabela[stevilo_vrstice].append(0)
            portal_par = self.portali.get(znak, [])
            portal_par.append((x_koordinata, y_koordinata))
            self.portali[znak] = portal_par
          # Cekini
          elif znak == 'c':
            self.tabela[stevilo_vrstice].append(0)
            self.cekini.append((x_koordinata, y_koordinata))
          # Bombon, ki z vso svojo energijo žre duhove
          elif znak == 'b':
            self.tabela[stevilo_vrstice].append(0)
            self.bomboni.append((x_koordinata, y_koordinata))
          # Duhec
          elif znak == 'd':
            self.tabela[stevilo_vrstice].append(0)
            self.duhci.append((x_koordinata, y_koordinata))
          x_koordinata += 1
        y_koordinata += 1
        stevilo_vrstice += 1
    self.visina = stevilo_vrstice
    self.sirina = len(self.tabela[0])

  def __str__(self):
    rob = "+{}+".format(self.sirina * '--')
    prezentacija = rob + '\n'
    for vrstica in self.tabela:
      prezentacija_vrstice = ''
      for polje in vrstica:
        if polje == POLJE_PRAZNO:
          prezentacija_vrstice += '  '
        elif polje == POLJE_ZID:
          prezentacija_vrstice += '**'
      prezentacija += "|{}|\n".format(prezentacija_vrstice)
    prezentacija += rob
    return prezentacija

class Igra:
  def __init__(self, ime_povrsine):
    self.povrsina = Povrsina(ime_povrsine)
    self.pakman = Pakman((8, 11))
    self.pakman.nastavi_smer(LEVO)
    self.naslednja_smer = LEVO
    self.rezultat = 0
    self.duhci = []
    self.obratna_igra = False
    for duhec in self.povrsina.duhci:
      duh = Pakman(duhec)
      duh.nastavi_smer(GOR)
      self.duhci.append(duh)
  
  def spremeni_smer(self, kam):
    if self.pakman.smer == LEVO and kam == DESNO:
      self.pakman.nastavi_smer(DESNO)   
    elif self.pakman.smer == DESNO and kam == LEVO:
      self.pakman.nastavi_smer(LEVO)
    elif self.pakman.smer == GOR and kam == DOL:
      self.pakman.nastavi_smer(DOL)   
    elif self.pakman.smer == DOL and kam == GOR:
      self.pakman.nastavi_smer(GOR)
    self.naslednja_smer = kam

  def razdalja(self, pakman, duhec):
    px, py = pakman
    dx, dy = duhec
    return math.pow((px-dx)**2 + (py - dy)**2, 1/2)

  def lahko_premakne(self, tocka):
    x, y = tocka
    x = int(round(x))
    y = int(round(y))
    if not (0 <= x < self.povrsina.sirina and 0 <= y < self.povrsina.visina):
      return False
    if self.povrsina.tabela[y][x] == POLJE_ZID:
      return False
    return True

  def celostevilske_koordinate(self, koordinate):
    x, y = koordinate
    return round(x, 2) == int(round(x, 2)) and round(y, 2) == int(round(y,2))

  def pojej_cekin(self, pozicija):
    poz_x, poz_y = pozicija
    index = self.povrsina.cekini.index((poz_x, poz_y))
    del self.povrsina.cekini[index]
    self.rezultat += 100

  def pojej_bombon(self, pozicija):
    poz_x, poz_y = pozicija
    index = self.povrsina.bomboni.index((poz_x, poz_y))
    del self.povrsina.bomboni[index]
    self.rezultat += 500
    self.obratna_igra = True

  def korak(self):
    for duhec in self.duhci:
      # Preblizu AJS
      if self.razdalja(self.pakman.pozicija, duhec.pozicija) < 1:
        return False

    if self.celostevilske_koordinate(self.pakman.pozicija):
      if self.lahko_premakne(self.pakman.premik_kam(self.naslednja_smer)):
        self.pakman.nastavi_smer(self.naslednja_smer)
        self.pakman.premik()
      elif self.lahko_premakne(self.pakman.premik_kam(self.pakman.smer)):
        self.pakman.premik()
    else:
      self.pakman.premik()

    for duhec in self.duhci:
      if self.celostevilske_koordinate(duhec.pozicija):
        duhcova_odlocitev = random.randint(1,1)
        # Butast duhec naredi random potezo
        if duhcova_odlocitev == 1:
          while True:
            smer = random.choice([GOR, DOL, LEVO, DESNO])
            if self.lahko_premakne(duhec.premik_kam(smer)):
              duhec.nastavi_smer(smer)
              duhec.premik()
              break    
      else:
        duhec.premik()

    # Če je na portalu ga prestavi
    if self.celostevilske_koordinate(self.pakman.pozicija):
      poz_x, poz_y = self.pakman.pozicija
      poz_x = int(round(poz_x))
      poz_y = int(round(poz_y))
      if (poz_x, poz_y) in self.povrsina.cekini:
        self.pojej_cekin((poz_x, poz_y))
      if (poz_x, poz_y) in self.povrsina.bomboni:
        self.pojej_bombon((poz_x, poz_y))

      pozicija = (poz_x, poz_y)
      for ime_portala, par_tock in self.povrsina.portali.items():
        if pozicija in par_tock:
          preslikaj_v = (par_tock.index(pozicija) + 1) % 2
          self.pakman.pozicija = par_tock[preslikaj_v]
    return True


#TODO smer, pozicija
#a = Povrsina('povrsine/povrsina1.pak')
#print(a)