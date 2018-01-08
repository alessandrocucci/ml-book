# Errata Corrige
##### Errori nella prima stampa del volume *A tu per tu col **Machine Learning***

#### Introduzione
| **Pagina** | **Riga** | **Errata** | **Corrige** |
|------|------|------------|-------------|
| 2     | 16   | 2 Gb di RAM  | 32 Mb di RAM   |

#### Capitolo 1
| **Pagina** | **Riga** | **Errata** | **Corrige** |
|------|------|------------|-------------|
| 22     | 13   | `>>> d['nome']`  | `>>> dipendente['nome']`   |
| 23     | 29   | `>>> d.get(’anni_di_esperienza’, 0)`  | `>>> dipendente.get(’anni_di_esperienza’, 0)`   |
| 23     | 31   | `>>> print(d.get(’clienti_esterni’))`  | `>>> print(dipendente.get(’clienti_esterni’))`   |
| 31     | 6   | `l.append(x, y)`  | `l.append((x, y))`   |

#### Capitolo 2
| **Pagina** | **Riga** | **Errata** | **Corrige** |
|------|------|------------|-------------|
| 58     | 1   | `>>> l = [1, "ciao", False, []]`  | `>>> l = [1, "ciao", False]`   |
| 58     | 2   | `>>> a = np.array([1, "ciao", False, []])`  | `>>> a = np.array([1, "ciao", False])`   |
| 58     | 5   | `[<type ’int’>, <type ’str’>, <type ’bool’>, <type ’list’>]`  | `[<type ’int’>, <type ’str’>, <type ’bool’>]`   |
| 58     | 8   | `[<type ’numpy.string_’>, <type ’numpy.string_’>, <type ’numpy.string_’>, <type ’numpy.string_’>]`  | `[<type ’numpy.string_’>, <type ’numpy.string_’>, <type ’numpy.string_’>]`   |
| 63     | 3   | ` print i, elemento`  | ` print(i, elemento)`   |
| 63     | 16   | ` print i, elemento`  | ` print(i, elemento)`   |
| 63     | 30   | ` print el,`  | ` print(el, end=' ')`   |
| 64     | 1   | ` print el,`  | ` print(el, end=' ')`   |
| 64     | 5   | ` print el,`  | ` print(el, end=' ')`   |

# Aggiunte 
#### Capitolo 1
| **Pagina** | **Riga** | **Prima di** | **Aggiungere** |
|------|------|------------|-------------|
| 27     | 36   | `>>> while 0 < limite <= 5:`  | `>>> limite = 5`   |
