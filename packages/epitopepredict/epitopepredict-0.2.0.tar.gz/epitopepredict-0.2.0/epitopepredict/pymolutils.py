#!/usr/bin/env python

"""
    Module implementing peptide sequence/structure utilities.
    Created March 2013
    Copyright (C) Damien Farrell
"""

import os, sys, types
import colorsys
import random, math
import numpy as np
import pylab as plt
import shutil

redcolors=['red','tv_red','raspberry','darksalmon','ruby',
        'deepsalmon','warmpink','salmon','firebrick','chocolate','brown']
bluecolors=['blue','tv_blue','marine','slate','lightblue','skyblue',
        'purpleblue','deepblue','density']
yellowcolors=['yellow','tv_yellow','paleyellow','yelloworange','limon','wheat','sand']
pymolcolors = redcolors+bluecolors+yellowcolors
simplecolors = ['red','cyan','yellow','orange','magenta','blue']
home = os.path.expanduser("~")

def import_pymol():
    """Call this method at the start of every script instead of
    globally otherwise the pymol thread will be called when this
    module is imported"""

    #check if imported already
    if 'pymol' in list(sys.modules.keys()):
        return
    import __main__
    __main__.pymol_argv = [ 'pymol', '-qc']
    import pymol
    __main__.pymol = pymol
    import pymol.cmd
    global cmd
    cmd = pymol.cmd
    stdout = sys.stdout
    pymol.finish_launching()
    sys.stdout = stdout
    return cmd

def show_protein(filename, save=False):
    """Default protein display"""

    import_pymol()
    if not os.path.exists(filename):
        print 'no file %s' %filename
        return
    cmd.load(filename)
    nname = os.path.splitext(os.path.basename(filename))[0]
    cmd.color('limegreen')
    cmd.show('cartoon')
    cmd.hide('lines')
    cmd.hide('everything','resn hoh')
    cmd.bg_color('white')
    cmd.set('stick_radius',0.1)
    cmd.set('cartoon_fancy_helices', 1)
    cmd.set('cartoon_side_chain_helper', 1)
    #cmd.zoom('chain a', 1)
    cmd.orient()
    if save == True:
        cmd.save(nname+'.pse')
    #cmd.reinitialize()
    return

def save(name):
    cmd.save(name)

def save_image(filename):
    """Save a ray traced image from a project file"""

    import_pymol()
    cmd.load(filename)
    cmd.set('ray_trace_mode',3)
    name = os.path.splitext(os.path.basename(filename))[0]
    name = os.path.abspath(name)+'.png'
    cmd.png(name, 1000, 800, dpi=150, ray=1)
    cmd.quit()
    return

def show_sequences(seqs=None,coords=None,name='sequences'):
    """Show sequence locations on the protein"""

    offset=8

    import io
    s = (cmd.get_fastastr('all'))
    f = io.BytesIO(s)
    from Bio import SeqIO
    seq = SeqIO.read(f,'fasta').seq
    print seq
    coords=[]
    for s in seqs:
        ind = seq.find(s)+offset
        print s, ind
        coords.append((ind,len(s)))
    print coords
    if coords is not None:
        seqstr = [str(i[0])+'-'+str(i[0]+i[1]) for i in coords]
        seqstr = '+'.join(seqstr)
        print (seqstr)
    cmd.select(name, '( chain a and resi %s )' %seqstr)
    cmd.color('red', name)
    return

def find_surface_residues(objSel="(all)", cutoff=2.5, show=False, verbose=False):
    """
    findSurfaceResidues
        finds those residues on the surface of a protein
        that have at least 'cutoff' exposed A**2 surface area.

    PARAMS
        objSel (string)
            the object or selection in which to find
            exposed residues
            DEFAULT: (all)

        cutoff (float)
            your cutoff of what is exposed or not.
            DEFAULT: 2.5 Ang**2

        asSel (boolean)
            make a selection out of the residues found

    RETURNS
        (list: (chain, resv ) )
            A Python list of residue numbers corresponding
            to those residues w/more exposure than the cutoff.

    """
    from pymol import stored
    tmpObj="__tmp"
    cmd.create( tmpObj, objSel + " and polymer");
    if verbose!=False:
        print "WARNING: I'm setting dot_solvent.  You may not care for this."
    cmd.set("dot_solvent");
    cmd.get_area(selection=tmpObj, load_b=1)

    # threshold on what one considers an "exposed" atom (in A**2):
    cmd.remove( tmpObj + " and b < " + str(cutoff) )

    stored.tmp_dict = {}
    cmd.iterate(tmpObj, "stored.tmp_dict[(chain,resv)]=1")
    exposed = stored.tmp_dict.keys()
    exposed.sort()

    randstr = str(random.randint(0,10000))
    selName = "exposed_atm_" + randstr
    if verbose!=False:
        print "Exposed residues are selected in: " + selName
    cmd.select(selName, objSel + " in " + tmpObj )
    selNameRes = "exposed_res_" + randstr
    cmd.select(selNameRes, "byres " + selName )

    if show != False:
        cmd.show_as("spheres", objSel + " and poly")
        cmd.color("white", objSel)
        cmd.color("red", selName)
    cmd.delete(tmpObj)
    print exposed
    return exposed

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-t", "--test", dest="test", action='store_true',
                            help="test")

    opts, remainder = parser.parse_args()
    if opts.test == True:
        importPymol()
        pdbfile = '2o6x.pdb'
        show_protein(pdbfile, save=True)
        save_image('2o6x.pse')
