# -*- coding: utf-8 -*-

import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

sb.set()

def draw_plot(x_plot, session, generator_result, generator_placeholder, generator_batch, i, rrep_dstep, rrep_gstep, grep_dstep, grep_gstep):
    plt.figure()
    g_plot = session.run(generator_result, feed_dict={generator_placeholder: generator_batch})
    xax = plt.scatter(x_plot[:,0], x_plot[:,1])
    gax = plt.scatter(g_plot[:,0],g_plot[:,1])

    plt.legend((xax,gax), ("Real Data","Generated Data"))
    plt.title('Samples at Iteration %d'%i)
    plt.tight_layout()
    plt.savefig('plots/iterations/iteration_%d.png'%i)
    plt.close()

    plt.figure()
    rrd = plt.scatter(rrep_dstep[:,0], rrep_dstep[:,1], alpha=0.5)
    rrg = plt.scatter(rrep_gstep[:,0], rrep_gstep[:,1], alpha=0.5)
    grd = plt.scatter(grep_dstep[:,0], grep_dstep[:,1], alpha=0.5)
    grg = plt.scatter(grep_gstep[:,0], grep_gstep[:,1], alpha=0.5)


    plt.legend((rrd, rrg, grd, grg), ("Real Data Before G step","Real Data After G step",
                            "Generated Data Before G step","Generated Data After G step"))
    plt.title('Transformed Features at Iteration %d'%i)
    plt.tight_layout()
    plt.savefig('plots/features/feature_transform_%d.png'%i)
    plt.close()

    plt.figure()

    rrdc = plt.scatter(np.mean(rrep_dstep[:,0]), np.mean(rrep_dstep[:,1]),s=100, alpha=0.5)
    rrgc = plt.scatter(np.mean(rrep_gstep[:,0]), np.mean(rrep_gstep[:,1]),s=100, alpha=0.5)
    grdc = plt.scatter(np.mean(grep_dstep[:,0]), np.mean(grep_dstep[:,1]),s=100, alpha=0.5)
    grgc = plt.scatter(np.mean(grep_gstep[:,0]), np.mean(grep_gstep[:,1]),s=100, alpha=0.5)

    plt.legend((rrdc, rrgc, grdc, grgc), ("Real Data Before G step","Real Data After G step",
                            "Generated Data Before G step","Generated Data After G step"))

    plt.title('Centroid of Transformed Features at Iteration %d'%i)
    plt.tight_layout()
    plt.savefig('plots/features/feature_transform_centroid_%d.png'%i)
    plt.close()