require 'rspec'
require 'matrix'

class Matrix
  def []=(i, j, x)
    @rows[i][j] = x
  end
end

# This is where you implement your solution 
def convert_coordinates(agents)
  agents.map{ |position| [position[/[A-Z]+/].ord - 'A'.ord, position[/[0-9]+/].to_i - 1] }
end

def convert_coordinates_backwards(agents)
  agents.map{ |position| (position[0] + 'A'.ord).chr + (position[1] + 1).to_s }
end

def calculate_distance(a, b)
  (a[0] - b[0]).abs + (a[1] - b[1]).abs
end

def find_safe_spaces(agents)
  safe_spaces_by_position = Matrix.build(10, 10){|r, c| 100}
  agents = agents.select{|a| a[0] < 10 and a[1] < 10}

  for y in 0..9 do
    for x in 0..9 do
      for position in agents
        distance = calculate_distance(position, [x, y])
        #puts x.to_s + "," + y.to_s + ": " + distance.to_s
        safe_spaces_by_position[x, y] = distance if distance < safe_spaces_by_position[x, y]
      end
    end
  end

  max = 0
  for y in 0..9 do
    for x in 0..9 do
      max = safe_spaces_by_position[x, y] if safe_spaces_by_position[x, y] > max
    end
  end

  result = []
  if max > 0
    for x in 0..9 do
      for y in 0..9 do
        result << [x, y] if safe_spaces_by_position[x, y] == max
      end
    end
  end

  return result
end

def advice_for_alex(agents)
  results = find_safe_spaces(convert_coordinates(agents))

  return 'The whole city is safe for Alex! :-)' if agents.size == 0 or results.size == 100
  return 'There are no safe locations for Alex! :-(' if results.size == 0

  return convert_coordinates_backwards(results)
end

# Please enable Level 1, 2, 3-Tests by replacing xdescribe with describe!
# Do not edit the tests itself!
RSpec.describe 'Spy Places Level 1 - convert coordinates' do
  it 'no agents return empty array' do
    agents = []
    expect(convert_coordinates(agents)).to match_array([])
  end

  it 'one agent casts to array' do
    agents =
        ['F3']
    expect(convert_coordinates(agents)).to match_array([[5, 2]])
  end

  it 'some agents casts to array' do
    agents =
        ['B6', 'C2', 'J7']
    expect(convert_coordinates(agents)).to match_array([[1, 5], [2, 1], [9, 6]])
  end

  it 'handle two digits' do
    agents =
        ['J10']
    expect(convert_coordinates(agents)).to match_array([[9, 9]])
  end
end

RSpec.describe 'Spy Places Level 2 - find save places' do
  it 'some places are save if agents are some' do
    agents =
        [[1, 1], [3, 5], [4, 8], [7, 3], [7, 8], [9, 1]]
    expect(find_safe_spaces(agents)).to match_array([[0, 9], [0, 7], [5, 0]])
  end
  it 'some places are save if agents are some' do
    agents =
        [[0, 0], [0, 9], [1, 5], [5, 1], [9, 0], [9, 9]]
    expect(find_safe_spaces(agents)).to match_array([[5, 7], [6, 6], [7, 5]])
  end
  it 'one place is save' do
    agents =
        [[0, 0]]
    expect(find_safe_spaces(agents)).to match_array([[9, 9]])
  end
end

RSpec.describe 'Spy Places Level 3 - find edge cases and give advice to Alex' do
  it 'expects all save places at no agents' do
    agents = []
    expect(advice_for_alex(agents)).to eq('The whole city is safe for Alex! :-)')
  end

  it 'no place is save if agents are everywhere' do
    agents =
        ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
         'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
         'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
         'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
         'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
         'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
         'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
         'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
         'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10',
         'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10']
    expect(advice_for_alex(agents)).to eq('There are no safe locations for Alex! :-(')
  end

  it 'some places are save if agents are some' do
    agents =
        ['B2', 'D6', 'E9', 'H4', 'H9', 'J2']
    expect(advice_for_alex(agents)).to match_array(['A10', 'A8', 'F1'])
  end
  it 'some places are save if agents are some' do
    agents =
        ['B4', 'C4', 'C8', 'E2', 'F10', 'H1', 'J6']
    expect(advice_for_alex(agents)).to match_array(['A1', 'A10', 'E6', 'F5', 'F6', 'G4', 'G5', 'G7', 'H8', 'I9', 'J10'])
  end
  it 'some places are save if agents are some' do
    agents =
        ['A1', 'A10', 'B6', 'F2', 'J1', 'J10']
    expect(advice_for_alex(agents)).to match_array(['F8', 'G7', 'H6'])
  end
  it 'one save place' do
    agents =
        ['A1']
    expect(advice_for_alex(agents)).to match_array(['J10'])
  end
  it 'agent outside the city' do
    agents =
        ['A12']
    expect(advice_for_alex(agents)).to eq('The whole city is safe for Alex! :-)')
  end
end