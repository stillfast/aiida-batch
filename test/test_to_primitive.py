#!/usr/bin/env python3
"""Test script to verify to_primitive parameter behavior.

Usage:
    python test/test_to_primitive.py
"""

import sys
sys.path.insert(0, 'src')

from aiida_batch.utils.structure import generate_by_protos

def test_to_primitive():
    """Test that to_primitive parameter works correctly."""
    
    print("=" * 60)
    print("Testing to_primitive parameter behavior")
    print("=" * 60)
    
    protos = ["BCC", "FCC", "Alpha-U"]
    element = "U"
    
    # Test with to_primitive=False
    print("\n--- to_primitive=False ---")
    structures_not_primitive = generate_by_protos(
        protos=protos,
        element=element,
        to_primitive=False,
    )
    
    print("\nStructures WITHOUT primitive conversion:")
    for name, atoms in structures_not_primitive.items():
        print(f"  {name}: {len(atoms)} atoms")
    
    # Test with to_primitive=True
    print("\n--- to_primitive=True ---")
    structures_primitive = generate_by_protos(
        protos=protos,
        element=element,
        to_primitive=True,
    )
    
    print("\nStructures WITH primitive conversion:")
    for name, atoms in structures_primitive.items():
        print(f"  {name}: {len(atoms)} atoms")
    
    # Compare
    print("\n--- Comparison ---")
    all_match = True
    for proto in protos:
        if proto in structures_not_primitive and proto in structures_primitive:
            natoms_not_prim = len(structures_not_primitive[proto])
            natoms_prim = len(structures_primitive[proto])
            
            is_primitive = natoms_prim < natoms_not_prim
            
            print(f"  {proto}:")
            print(f"    Conventional: {natoms_not_prim} atoms")
            print(f"    Primitive:   {natoms_prim} atoms")
            print(f"    Correctly converted: {is_primitive}")
            
            if natoms_not_prim == natoms_prim:
                print(f"    WARNING: No difference between primitive and conventional!")
                all_match = False
    
    print("\n" + "=" * 60)
    if all_match:
        print("TEST PASSED: to_primitive parameter works correctly!")
    else:
        print("TEST FAILED: to_primitive parameter may not be working!")
    print("=" * 60)
    
    return all_match


if __name__ == "__main__":
    success = test_to_primitive()
    sys.exit(0 if success else 1)
