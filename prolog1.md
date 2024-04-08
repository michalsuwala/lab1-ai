#### Zadanie 1.1

A - x i y są rodzeństwem

B - x i y są kuzynami

C - x i y są dziadkami tego samego wnuczka

D - y jest przyrodnim rodzicem x, x jest przyrodnim dzieckiem y

E - x i y są przyrodnim rodzeństwem

F - x i y są dla siebie szwagrami

G - X i y są przyrodnim rodzeństwem


Zadanie 1.2

dziadek(X, Z) :- rodzic(X, Y), rodzic(Y, Z).

rodzenstwo(X, Y) :- 
    rodzic(X, Z), 
    rodzic(Y, Z), 
    rodzic(X, M), 
    rodzic(Y, M).

rodzenstwo_przyrodnie(X, Y) :- rodzic(X, Z), rodzic(Y, Z).

kuzyn(X, Y) :- 
    rodzic(X, A),
    rodzic(Y, B),
    rodzenstwo_przyrodnie(A, B).

dziadkowie(X, Y) :- dziadek(M, X), dziadek(M, Y).

przyrodni_rodzic(X, Y) :- 
    rodzic(X, Z),
    rodzic(M, Z),
    rodzic(M, Y).
    
szwagier(X, Y) :-
    rodzic(Z, X),
    dziadek(Z, M),
    rodzic(Y, M).

rodzenstwo_przyrodnie_g(X, Y) :-
    rodzenstwo_przyrodnie(X, Y),
    dziadek(Y, Z),
    rodzic(X, Z).


#### Zadanie 2

mezczyzna(a).\
osoba(b).\
rodzic(a, b).\
rodzic(y, z).\
rodzic(x, y).\
rodzic(x, a).\

kobieta(X) :- osoba(X), not(mezczyzna(x)).

ojciec(X, Y) :- mezczyzna(X), rodzic(X, Y).

matka(X, Y) :- kobieta(X), rodzic(X, Y).

corka(X, Y) :- kobieta(X), rodzic(Y, X).

brat_rodzony(X, Y) :- 
    ojciec(M, X),
    ojciec(M, Y),
    matka(N, X),
    matka(N, Y).

brat_przyrodni(X, Y) :-
    rodzic(M, X),
    rodzic(M, Y),
    not(brat_rodzony(X, Y)).

kuzyn(X, Y) :-
    rodzic(M, X),
    rodzic(N, Y),
    (   brat_rodzony(M, N);
    brat_przyrodni(M, N)).

dziadek_od_strony_ojca(X,Y) :-
    ojciec(Z, Y),
    ojciec(X, Z).

dziadek_od_strony_matki(X,Y) :-
    matka(Z, Y),
    ojciec(X, Z).

dziadek(X,Y) :-
    rodzic(Z, Y),
    ojciec(X, Z).

babcia(X,Y) :-
    rodzic(Z, Y),
    matka(X, Z).

wnuczka(X,Y) :-
    babcia(Y, X),
    kobieta(X).

przodek_do2pokolenia_wstecz(X,Y) :-
    dziadek(X, Y);
    babcia(X, Y).

przodek_do3pokolenia_wstecz(X,Y) :-
    (   dziadek(Z, Y);
    babcia(Z, Y)),
    rodzic(X, X).


#### Dla chętnych 1

drzwi(a, b).
drzwi(b, c).
drzwi(b, d).
drzwi(d, e).
drzwi(e, f).

klucz(e, kluczE).
klucz(d, kluczD).

otwiera(f, kluczE).


:- dynamic visited/1, vis/1, vis2/1, found/0, klucze/1.


szukaj_wyjscia(POKOJ_POCZATKOWY, POKOJ_Z_KLUCZEM, KLUCZ, POKOJ_Z_WYJSCIEM) :-
    retractall(visited(_)),
    szukaj(POKOJ_POCZATKOWY, POKOJ_Z_KLUCZEM, KLUCZ, POKOJ_Z_WYJSCIEM).


szukaj(POKOJ, _, _, _) :-
    visited(POKOJ), !, fail.

szukaj(POKOJ, POKOJ_Z_KLUCZEM, KLUCZ, POKOJ_Z_WYJSCIEM) :-
    (POKOJ = POKOJ_Z_KLUCZEM ;
    klucze(POKOJ);
    klucz(POKOJ, KL) -> write('[znalazlem_klucz, '), write(KL), write(']'), nl, assert(klucze(POKOJ))
    ),
    assert(visited(POKOJ)),
    (POKOJ = POKOJ_Z_KLUCZEM -> write('[znalazlem_klucz, '), write(KLUCZ), write(']'), nl, assert(found), 
    szukajw_tyl(POKOJ, POKOJ_Z_WYJSCIEM)
    ).

szukaj(POKOJ_POCZATKOWY, POKOJ_Z_KLUCZEM, KLUCZ, POKOJ_Z_WYJSCIEM) :-
    found;
    drzwi(POKOJ_POCZATKOWY, POKOJ),
    write('[przechodze_z, '), write(POKOJ_POCZATKOWY), write(', do, '), write(POKOJ), write(']'), nl,
    szukaj(POKOJ, POKOJ_Z_KLUCZEM, KLUCZ, POKOJ_Z_WYJSCIEM).


szukajw_przod(POKOJ, _) :-
    vis(POKOJ), !, fail.

szukajw_przod(POKOJ_Z_KLUCZEM, POKOJ_Z_WYJSCIEM) :-
    (POKOJ_Z_WYJSCIEM = POKOJ_Z_KLUCZEM ->  
    write("WYJSCIE"), 
    found);
    assert(vis(POKOJ_Z_KLUCZEM)),
    drzwi(POKOJ_Z_KLUCZEM, POKOJ),
    write('[przechodze_z, '), write(POKOJ_Z_KLUCZEM), write(', do, '), write(POKOJ), write(']'), nl,
    szukajw_przod(POKOJ, POKOJ_Z_WYJSCIEM).


szukajw_tyl(POKOJ, _) :-
    vis2(POKOJ), !, fail.

szukajw_tyl(POKOJ_Z_KLUCZEM, POKOJ_Z_WYJSCIEM) :-
    (POKOJ_Z_WYJSCIEM = POKOJ_Z_KLUCZEM -> 
    write("WYJSCIE"),
    found);
    assert(vis2(POKOJ_Z_KLUCZEM)),
    drzwi(POKOJ, POKOJ_Z_KLUCZEM),
    write('[przechodze_z, '), write(POKOJ_Z_KLUCZEM), write(', do, '), write(POKOJ), write(']'), nl,
    szukajw_przod(POKOJ, POKOJ_Z_WYJSCIEM);
    drzwi(POKOJ, POKOJ_Z_KLUCZEM),    
    szukajw_tyl(POKOJ, POKOJ_Z_WYJSCIEM).


?- szukaj_wyjscia(a, e, kluczE, f).



#### Dla chętnych 2

Zadanie 1\
a)\
Stałe indywidualne:
* Markus
* Cezar\

Predykaty:
* człowiek
* Pompejańczyk
* Rzymianin
* władca
* lojalność
* nienawiść
* zamach\


* czlowiek(Markus)
* pompejanczyk(Markus)
* ∀x(pompejanczyk(x)) -> rzymianin(X)
* wladca(Cezar)
* ∀x(rzymianin(x) -> (lojalnosc(x, Cezar) ∨ nienawisc(x, Cezar)))
* ∀x ∃y(lojalny(x, y))
* (zamach(x, y) ∧ wladca(y) ∧ czlowiek(x)) -> ∼lojalnosc(x, y)
* zamach(Markus, Cezar)\

b)\
(zamach(Markus, Cezar) ∧ wladca(Cezar) ∧ czlowiek(Markus)) -> ∼lojalnosc(Markus, Cezar)\
Markus nie był lojalny wobec Cezara.\

c)
* czlowiek(Markus)
* pompejanczyk(Markus)
* ∀x(∼pompejanczyk(x) ∨  rzymianin(X))
* wladca(Cezar)
* ∀x(∼rzymianin(x) ∨ lojalnosc(x, Cezar) ∨ nienawisc(x, Cezar))
* ∀x ∃y(lojalny(x, y))
* ∼zamach(x, y) ∨ ∼wladca(y) ∨ ∼czlowiek(x) ∨ ∼lojalnosc(x, y)
* zamach(Markus, Cezar)\

d)\
Dodajemy negację ∼lojalnosc(Markus, Cezar)\
1.\
    ∼zamach(Markus, Cezar) ∨ ∼wladca(Cezar) ∨ ∼czlowiek(Markus) ∨ ∼lojalnosc(Markus, Cezar)\
    zamach(Markus, Cezar)\
    wladca(Cezar)\
    czlowiek(Markus)\
    lojalnosc(Markus, Cezar)\
2.\
    ∼wladca(Cezar) ∨ ∼czlowiek(Markus) ∨ ∼lojalnosc(Markus, Cezar)\
    wladca(Cezar)\
    czlowiek(Markus)\
    lojalnosc(Markus, Cezar)\
3.\
    ∼czlowiek(Markus) ∨ ∼lojalnosc(Markus, Cezar)\
    czlowiek(Markus)\
    lojalnosc(Markus, Cezar)\
4.\
    ∼lojalnosc(Markus, Cezar)\
    lojalnosc(Markus, Cezar)\
5. \
    Zostaje zbiór pusty, co pokazuje, że Markus nie jest lojalny wobec Cezara.\


Zadanie 2\

a)
* ∀x(pozywienie(x) -> lubi(Jan, x)
* pozywienie(jablka)
* pozywienie(kurczak)
* ∀x,y(je(x, y) ∧ ∼zabija(y, x) -> pozywienie(y))
* je(Adam, orzeszki) ∧ ∼zabija(orzeszki, Adam)
* ∀x(je(Adam, x) -> je(Basia, x))\

b)
* ∀x(∼pozywienie(x) ∨ lubi(Jan, x)
* pozywienie(jablka)
* pozywienie(kurczak)
* ∀x,y(∼je(x, y) ∨ zabija(y, x) ∨ pozywienie(y))
* ∼(∼je(Adam, orzeszki) ∨ zabija(orzeszki, Adam))
* ∀x(∼je(Adam, x) ∨ je(Basia, x))\

c)\
Dodajemy negację pozywienie(orzeszki)\
1. \
    je(Adam, orzeszki) ∧ ∼zabija(orzeszki, Adam)\
    ∼je(Adam, orzeszki) ∨ zabija(orzeszki, Adam) ∨ pozywienie(orzeszki)\
    ∼pozywienie(orzeszki)\
2.\
    ∼zabija(orzeszki, Adam)\
    zabija(orzeszki, Adam) ∨ pozywienie(orzeszki)\
    ∼pozywienie(orzeszki)\
3.\
    pozywienie(orzeszki))\
    ∼pozywienie(orzeszki)\
4. \
    Zostaje zbiór pusty, co pokazuje, że pozywienie(orzeszki).\

    Teraz wiedząc, że ∼pozywienie(orzeszki) ∨ lubi(Jan, orzeszki) możemy wywnioskować, że Jan lubi orzeszki.\

d)\
∼je(Adam, x) ∨ je(Basia, x)\
je(Adam, orzeszki) 

1.\
    ∼je(Adam, orzeszki) ∨ je(Basia, orzeszki)\
    je(Adam, orzeszki)\
    ∼je(Basia, orzeszki)\
2.\
    je(Basia, orzeszki)\
    ∼je(Basia, orzeszki)\
3.\
    Zostaje zbiór pusty, czyli Basia je orzeszki.


Zadanie 4

1. narodziny(Markus, 40)
2. zniszczenie(Pompeje, 79)
3. ∀x ∃y,q,z((narodziny(x, y) ∧ zniszczenie(Pompeje, z) ∧ y <= z) -> ~zyje(x, q))
4. ∀x ∃y,q,z((zyje(x, y) ∧ zniszczenie(Pompeje, z) ∧ y > z) -> narodziny(x, q) ∧ y - q <= 150)

Można to wykazać na dwa sposoby:\

a) Z użyciem 3 podpunktu - Markus narodził się przed zniszeniem Pompejów, co implikuje, że nie żyje.\

b) Z użyciem 4 podpunktu - narodziny Markusa i rok 2021 dzieli więcej niż 150 lat, czyli wartość po implikacji
ma wartość 0. To znaczy, że wartość przed implikacją również musi posiadać wartość 0. Rok 2021 jest po zniszczeniu 
Pompejów, czyli stwierdzenie, że Markus żyje w roku 2021 jest nieprawdziwe.
