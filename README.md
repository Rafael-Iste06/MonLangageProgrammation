# Mon Langage de Programmation

Un langage de programmation simple avec des types personnalisés : `Tree`, `Stack`, et `Queue`.

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/Rafael-Iste06/MonLangageProgrammation.git
   cd MonLangageProgrammation
   ```

2. Exécutez un script :
   ```bash
   python main.py
   ```

## Syntaxe de Base

- **Variables** : `x = 10`
- **Conditions** :
  ```python
  if x > 0:
      print("Positif")
  else:
      print("Négatif ou nul")
  ```
- **Boucles** :
  ```python
  while x > 0:
      x = x - 1
  ```
- **Fonctions** :
  ```python
  def fact(n):
      if n == 0:
          return 1
      else:
          return n * fact(n - 1)
  ```

## Types Personnalisés

- **Stack** :
  ```python
  s = Stack()
  s.push(1)
  s.push(2)
  print(s.pop())  # Affiche 2
  ```

- **Queue** :
  ```python
  q = Queue()
  q.enqueue(1)
  q.enqueue(2)
  print(q.dequeue())  # Affiche 1
  ```

- **Tree** :
  ```python
  root = TreeNode(1)
  child = TreeNode(2)
  root.add_child(child)
  ```

## Exemples

Voir le dossier `examples/` pour des exemples complets.