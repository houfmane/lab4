class Item:

  def __init__(self, code, weight, value):
    self.code = code
    self.weight = weight
    self.value = value


def knapsack(items, capacity):
  def node_bound_count(i, weight, value):
    if weight > capacity:
      return 0
    node_value = value
    j = i
    total_weight = weight

    while j < len(items) and total_weight + items[j].weight <= capacity:
      node_value += items[j].value
      total_weight += items[j].weight
      j += 1
    if j < len(items):
      node_value += (capacity - total_weight) * (
          items[j].value / items[j].weight
      )

    return node_value

  def branch_bound(i, weight, value, current_items):
    nonlocal max_value, best_items
    if weight <= capacity and value > max_value:
      max_value = value
      best_items = current_items[:]  # Сохраняем копию лучшего набора

    if i == len(items):
      return 0

    if node_bound_count(i, weight, value) > max_value:
      branch_bound(i + 1, weight, value, current_items)

    if (
        value + (capacity - weight) * (items[i].value / items[i].weight)
        > max_value
    ):
      current_items.append(items[i])
      branch_bound(
          i + 1, weight + items[i].weight, value + items[i].value, current_items
      )
      current_items.pop()

  items = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
  max_value = 0
  best_items = []
  branch_bound(0, 0, 0, [])
  return max_value, best_items


def build_grid(chosen_items, rows=3, cols=3):
  grid = [[None] * cols for _ in range(rows)]
  sorted_items = sorted(chosen_items, key=lambda x: x.weight, reverse=True)

  for item in sorted_items:
    placed = False
    for r in range(rows):
      for c in range(cols):
        if grid[r][c] is None:
          if item.weight == 2:
            if c + 1 < cols and grid[r][c + 1] is None:
              grid[r][c] = grid[r][c + 1] = item.code
              placed = True

            elif r + 1 < rows and grid[r + 1][c] is None:
              grid[r][c] = grid[r + 1][c] = item.code
              placed = True
          else:
            grid[r][c] = item.code
            placed = True
        if placed:
          break
      if placed:
        break

  return grid



if __name__ == '__main__':
  items = [
      Item('r', 3, 25),
      Item('p', 2, 15),
      Item('a', 2, 15),
      Item('m', 2, 20),
      Item('i', 1, 5),
      Item('k', 1, 15),
      Item('x', 3, 20),
      Item('t', 1, 25),
      Item('f', 1, 15),
      Item('d', 1, 10),
      Item('s', 2, 20),
      Item('c', 2, 20),
  ]

  capacity = 9
  start_score = 10
  total_items_score = sum(item.value for item in items)

  raw_value, chosen_items = knapsack(items, capacity)
  final_score = raw_value * 2 + start_score - total_items_score

  cols = 3
  rows = 3
  if final_score > 0:
    inventory = build_grid(chosen_items, rows, cols)
    for row in range(rows):
      print(inventory[row])
    print('Итоговые очки выживания:', final_score)
  else:
    print('Решения с положительным счётом не существует.')

  raw_value, chosen_items = knapsack(items, 7)
  final_score = raw_value * 2 + start_score - total_items_score

  print('\nДоп задание')

  if final_score > 0:
    inventory = build_grid(chosen_items, rows, cols)
    for row in range(rows):
      print(inventory[row])
    print('Итоговые очки выживания:', final_score)
  else:
    print('Решения с положительным счётом не существует.')


